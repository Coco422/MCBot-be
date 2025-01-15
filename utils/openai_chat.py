import httpx
from langchain_openai import ChatOpenAI
from services.chat_tools_impl import tools
from services.chat_tools_pydantic import tools_parse
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
import os
from typing import List, Dict, AsyncIterator
import json
import time


import openai

async def get_chat_response_stream_oai(messages: List[Dict[str, str]], system_prompt: str = "") -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应。
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    # 初始化 OpenAI 客户端
    api_key=os.getenv("ai_api_key")
    base_url=os.getenv("ai_base_url")
    model_id=os.getenv("ai_chat_model")


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
                        print(content, end="", flush=True)  # 打印机效果逐字符输出
                        yield f"event: Update\ndata: {content}\n\n"
                except json.JSONDecodeError:
                    # 如果 JSON 不完整，等待下一行继续拼接
                    continue
                except Exception as e:
                    print(f"意外错误: {e}, 缓存数据: {buffer}")
                    buffer = ""  # 避免死循环，清空缓存

    if buffer.strip():
        print(f"未处理的剩余数据: {buffer.strip()}")
    


async def get_chat_response_stream(messages: List[Dict[str, str]], system_prompt: str = "") -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应。
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    # 初始化 LangChain 的 ChatOpenAI
    llm = ChatOpenAI(
        model=os.getenv("ai_chat_model"),
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("ai_api_key"),
        base_url=os.getenv("ai_base_url"),
    )
        
    # 假如方法中传入参数system prompt 则在 messages 最前面加上，否则加上默认提示词
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
    print("now begin stream llm")
    start_time = time.time()
    flag = 1
    
    # 获取流式响应（同步生成器）
    for chunk in llm.stream(messages, stream_usage=True):
        if flag==1:
            end_time = time.time()
            print(end_time-start_time)
            full = chunk
            flag=0
        print("update")
        full += chunk
        yield f"event: Update\ndata: {chunk.content}\n\n" # 假设 AIMessageChunk 有 content 属性
        # await asyncio.sleep(0)  # 让出控制权，避免阻塞事件循环 效果有限。
    response_dict = {
    "content": full.content,
    "additional_kwargs": full.additional_kwargs,
    "response_metadata": full.response_metadata,
    "id": full.id,
    "usage_metadata": full.usage_metadata
    }
    # 将字典转换为 JSON 字符串
    json_string = json.dumps(response_dict, ensure_ascii=False)
    yield f"event: Done\ndata: {json_string}\n\n"