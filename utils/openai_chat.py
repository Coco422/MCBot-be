from langchain_openai import ChatOpenAI
import os
from typing import List, Dict, AsyncIterator
import asyncio
import json

async def get_chat_response(messages: List[Dict[str, str]], system_prompt: str = None) -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应。
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :param system_prompt: 系统提示词（可选），如果提供，会插入到 messages 的最前面
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
    
    # 如果提供了 system_prompt，插入到 messages 的最前面
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    
    # 获取流式响应（同步生成器）
    stream_res = llm.stream(messages, stream_usage=True)
    full = next(stream_res)
    # 将同步生成器转换为异步生成器
    for chunk in stream_res:
        full += chunk
        chunk_str = json.dumps({"AI_msg":chunk.content}, ensure_ascii=False)
        # print(chunk_str)
        yield chunk_str # 假设 AIMessageChunk 有 content 属性
        await asyncio.sleep(0)  # 让出控制权，避免阻塞事件循环
    response_dict = {
    "content": full.content,
    "additional_kwargs": full.additional_kwargs,
    "response_metadata": full.response_metadata,
    "id": full.id,
    "usage_metadata": full.usage_metadata
    }
    # 将字典转换为 JSON 字符串
    json_string = json.dumps(response_dict, ensure_ascii=False)
    yield (json_string)