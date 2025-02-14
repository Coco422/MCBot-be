
from typing import List, Dict, AsyncIterator
import httpx
import os

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------

async def get_chat_response_stream_langchain(messages: List[Dict[str, str]], system_prompt: str = "", model_name: str="hw_ai_chat_model_32", if_r1: bool=False) -> AsyncIterator[str]:
    """
    获取 OpenAI 聊天模型的流式响应
    :param messages: 聊天消息列表，格式为 [{"role": "system"|"user"|"assistant", "content": "消息内容"}, ...]
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
        # 替代方法get_chat_response_stream_langchain
        # 1. 构造请求体
        # 2. 发送请求
        # 3. 返回响应
    payload = {
        "messages": messages,
        "system_prompt": system_prompt,
        "model_name": model_name,
        "if_r1": if_r1
    }
    headers = {
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        async with client.stream("POST",os.getenv("MCBot_api_ai_url"), headers=headers, json=payload) as response:
            response.raise_for_status()
            buffer = ""  # 缓存跨行 JSON 数据
            async for line in response.aiter_lines():
                if not line:  # 跳过空行
                    continue
                try:
                    # 每个 event 和 data 都需要正确解析和处理
                    if line.startswith('event:'):
                        event = line[len('event:'):].strip()  # 提取 event 信息并去除空格
                    elif line.startswith('data:'):
                        data = line[len('data:'):].strip()  # 提取 data 信息并去除空格

                        # 如果缓冲区中已存在部分 data，说明当前行属于同一个数据包的部分内容
                        if buffer:
                            buffer += data
                        else:
                            buffer = data  # 如果是新的一段数据

                    # 检查是否有完整的数据包（包含 event 和 data）
                    if event and buffer:
                        yield f"event:{event}\ndata:{buffer}\n\n"  # 构建完整的 SSE 数据包
                        buffer = ""  # 清空缓存，以准备处理下一个数据包

                except Exception as e:
                    print(f"意外错误: {e}, 缓存数据: {buffer}")
                    buffer = ""  # 清空缓存，避免死循环