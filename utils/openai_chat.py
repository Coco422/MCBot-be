from langchain_openai import ChatOpenAI
from services.chat_tools_impl import tools
from services.chat_tools_pydantic import tools_parse
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
import os
from typing import List, Dict, AsyncIterator
import json

async def get_chat_response_stream(messages: List[Dict[str, str]]) -> AsyncIterator[str]:
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

    # 拥有 tools 列表的对象
    llm_with_tools = llm.bind_tools(tools)
    
    

    # 获取流式响应（同步生成器）
    stream_res = llm.stream(messages, stream_usage=True)
    full = next(stream_res)
    for chunk in stream_res:
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