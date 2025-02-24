import httpx
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from services.chat_tools_impl import tools
from services.chat_tools_pydantic import tools_parse
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
import os
from typing import List, Dict, AsyncIterator
import json
import time

from tools.utils import deprecated

from openai import AsyncOpenAI, OpenAI

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------

@deprecated
async def get_chat_response_stream_httpx(messages: List[Dict[str, str]], system_prompt: str = "") -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应。by httpx
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    api_key=os.getenv("ray_ai_api_key_default")
    base_url=os.getenv("ray_ai_base_url")
    model_id=os.getenv("hw_ai_chat_model_72")


    # 假如方法中传入参数 system prompt 则在 messages 最前面加上，否则加上默认提示词
    if not system_prompt and messages[0]["role"] != "system":
        system_message = {
            "role": "system",
            "content": "You are an AI assistant that helps people with their questions."
        }
        messages.insert(0, system_message)
    else:
        system_message = {
            "role": "system",
            "content": system_prompt
        }
        messages.insert(0, system_message)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.7,
        "stream": True,
    }

    print("now begin stream llm")
    start_time = time.time()
    flag = 1
    async with httpx.AsyncClient(timeout=10.0) as client:
        async with client.stream("POST", f"{base_url}/chat/completions", headers=headers, json=payload) as response:
            response.raise_for_status()  # 如果请求失败，抛出异常

            buffer = ""  # 缓存跨行 JSON 数据
            async for line in response.aiter_lines():
                if not line:  # 跳过空行
                    continue
                if flag == 1:
                    end_time = time.time()
                    print(end_time - start_time)
                    flag = 0
                buffer += line  # 将当前行添加到缓存
                if buffer.startswith("data: "):
                    buffer = buffer[len("data: "):]  # 移除 "data: " 前缀
                if buffer.strip() == "[DONE]":
                    buffer = ""  # 清空缓存
                    break
                try:
                    # 尝试解析完整的 JSON 数据
                    chunk = json.loads(buffer)
                    buffer = ""  # 清空缓存，解析成功

                    content = chunk.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    if content:  # 仅处理非空内容
                        yield f"event:update\ndata:{content}\n\n"
                        print(content, end="", flush=True)  # 打印机效果逐字符输出
                except json.JSONDecodeError:
                    # 如果 JSON 不完整，等待下一行继续拼接
                    continue
                except Exception as e:
                    print(f"意外错误: {e}, 缓存数据: {buffer}")
                    buffer = ""  # 避免死循环，清空缓存

    if buffer.strip():
        print(f"未处理的剩余数据: {buffer.strip()}")

@deprecated
async def get_chat_response_stream_asyoai(messages: List[Dict[str, str]], system_prompt: str = "") -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应。堵塞了
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    
    api_key=os.getenv("ray_ai_api_key_default")
    base_url=os.getenv("ray_ai_base_url")
    model_id=os.getenv("hw_ai_chat_model_72")

        # 假如方法中传入参数 system prompt 则在 messages 最前面加上，否则加上默认提示词
    if not system_prompt and messages[0]["role"] != "system":
        system_message = {
            "role": "system",
            "content": "You are an AI assistant that helps people with their questions."
        }
        messages.insert(0, system_message)

    client = AsyncOpenAI(base_url=base_url,api_key=api_key)
    # client = OpenAI(base_url=base_url,api_key=api_key)
    start_time = time.time()
    print(f"now begin stream llm: {start_time}")
    flag = 1
    completion = await client.chat.completions.create(
        model=model_id,
        messages=messages,
        stream=True,
        )
    async for chunk in completion:
        if flag == 1:
            ft_time = time.time()
            print(f"first token Consume time:{ft_time - start_time}")
            flag = 0
        print("in openai",end=":")
        print(chunk.choices[0].delta)
         # 实时推送数据到客户端
        yield f"event:update\ndata:{chunk.choices[0].delta.content}\n\n"
    end_time = time.time()
    print(f"all out put Consume time:{end_time - start_time}")

async def get_chat_response(messages: List[Dict[str, str]], system_prompt: str = "", if_json: bool = False) -> str:
    """
    获取 OpenAI 聊天模型的完整响应（非流式）
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :param system_prompt: 系统提示词
    :param if_json: 是否返回JSON格式的响应，如果为True则解析并返回SQL或SQL键的值
    :return: 返回完整的聊天响应内容或解析后的SQL语句
    """
    model_name = os.getenv("hw_ai_chat_model_72")
    logger.info(f"Using model: {model_name}")
    
    # 初始化 LangChain 的 ChatOpenAI
    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("ray_ai_api_key_default"),
        base_url=os.getenv("ray_ai_base_url"),
    )
    
    # 添加系统提示词
    if not system_prompt and messages[0]["role"] != "system":
        system_message = {
            "role": "system",
            "content": "You are an AI assistant that helps people with their questions."
        }
        messages.insert(0, system_message)
    else:
        system_message = {
            "role": "system",
            "content": system_prompt
        }
        messages.insert(0, system_message)

    start_time = time.time()
    try:
        # 配置chain
        if if_json:
            from langchain_core.output_parsers import JsonOutputParser
            chain = llm | JsonOutputParser()
            response = await chain.ainvoke(messages)
        else:
            response = await llm.ainvoke(messages)
        
        # 记录性能指标
        end_time = time.time()
        time_diff_ms = (end_time - start_time) * 1000
        logger.info(f"LLM response time: {time_diff_ms:.2f} ms")
        
        logger.debug(response.content if hasattr(response, 'content') else response)
    
        return response.content if hasattr(response, 'content') else response
    except Exception as e:
        logger.error(f"Error getting chat response: {str(e)}")
        raise

async def get_chat_response_stream_langchain(messages: List[Dict[str, str]], system_prompt: str = "", model_name: str="hw_ai_chat_model_32", if_r1: bool=False) -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    # 模型名根据传入参数从环境变量中获取，如果环境变量中没有则直接使用传入的参数
    model_name = os.getenv(model_name) if os.getenv(model_name) else model_name
    logger.info(model_name)
    if not os.getenv("GLOBAL_R1")=="True":
        if_r1=False

    if if_r1:
        # 针对 deepseek r1 系列的 reasoning_content 额外参数的处理
        llm = ChatDeepSeek(
            model=model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("ray_ai_api_key_default"),
            api_base=os.getenv("ray_ai_base_url"),
        )
    else:
        # 初始化 LangChain 的 ChatOpenAI
        llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("ray_ai_api_key_default"),
            base_url=os.getenv("ray_ai_base_url"),
        )
    # 假如方法中传入参数system prompt 则在 messages 最前面加上，否则加上默认提示词
    if not system_prompt and messages[0]["role"] != "system":
        system_message = {
            "role": "system",
            "content": "You are an AI assistant that helps people with their questions."
        }
        messages.insert(0, system_message)
    else:
        # logger.info(f"system_prompt: {system_prompt}")
        system_message = {
            "role": "system",
            "content": system_prompt
        }
        messages.insert(0, system_message)
    # print(messages)
    start_time = time.time()
    # 将时间戳转换为人类可读格式，精确到毫秒
    readable_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)) + f".{int(start_time * 1000) % 1000:03d}"
    logger.info(f"now begin stream llm: {readable_start_time}")
    flag = 1
    r1_think_flag = 0
    
    if if_r1:
        completion = llm.astream(messages)
    else:
        completion = llm.astream(messages, stream_usage=True)
    # 获取流式响应（异步生成器）
    async for chunk in completion:
        if flag == 1:
            ft_time = time.time()
            readable_ft_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ft_time)) + f".{int(ft_time * 1000) % 1000:03d}"
            time_diff_ms = (ft_time - start_time) * 1000  # 转换为毫秒
            logger.info(f"first token Consume time: {time_diff_ms:.2f} ms")
            logger.info(f"when we get first token from llm: {readable_ft_time}")
            full = chunk
            flag=0
        full += chunk

        if if_r1:
            if r1_think_flag==0:
                yield f"event:update\ndata:<think>\n\n"
                r1_think_flag=1
                print("开始思考")

            if chunk.content and r1_think_flag==2:
                r1_think_flag=3
                yield f"event:update\ndata:</think>\n\n"
                print("结束思考")

            if r1_think_flag==2 or chunk.additional_kwargs.get("reasoning_content"):
                r1_think_flag=2
                yield f"event:update\ndata:{chunk.additional_kwargs.get('reasoning_content')}\n\n"
                
            if r1_think_flag==3:
                yield f"event:update\ndata:{chunk.content}\n\n"
        else:
            yield f"event:update\ndata:{chunk.content}\n\n" # 假设 AIMessageChunk 有 content 属性

    end_time = time.time()
    readable_ft_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)) + f".{int(end_time * 1000) % 1000:03d}"
    time_diff_ms = (end_time - start_time) * 1000  # 转换为毫秒
    logger.info(f"when we get all token from llm: {readable_ft_time}")
    logger.info(f"all out put Consume time: {time_diff_ms:.2f} ms")
    if if_r1:
        response_dict = {
            "content": full.content,
            "response_metadata": full.response_metadata,
            "time_consuming": f"{time_diff_ms:.2f}"
        }
    else:
        response_dict = {
        "content": full.content,
        "response_metadata": full.response_metadata,
        "usage_metadata": full.usage_metadata,
        "time_consuming": f"{time_diff_ms:.2f}"
        }
    # 将字典转换为 JSON 字符串
    json_string = json.dumps(response_dict, ensure_ascii=False)
    yield f"event: Done\ndata:{json_string}\n\n"

