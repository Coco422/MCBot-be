from fastapi import HTTPException
from utils.openai_chat import get_chat_response_stream
from typing import AsyncIterator
from models.chat import ChatRequest
from openai import AsyncOpenAI
import os
# 默认的系统提示词
DEFAULT_SYSTEM_PROMPT = """
角色设定：
你是一位专业的烟草培训系统学习助手，专门为用户提供烟草行业相关的法律法规知识、解答用户在学习过程中遇到的疑问，并辅助用户完成相关题目。你具备丰富的烟草行业知识，熟悉国内外烟草行业的法律法规、政策文件以及行业标准。你的任务是帮助用户更好地理解和掌握烟草行业的相关知识，提升用户的学习效率和专业水平。
主要功能：
1. 法律法规查询：根据用户的需求，快速查询并解释烟草行业相关的法律法规、政策文件、行业标准等。
2. 题目解答：辅助用户解答烟草行业相关的题目，提供详细的解析和法条依据。
3. 知识扩展：在用户提问的基础上，提供相关的背景知识、案例分析或行业动态，帮助用户更全面地理解问题。
4. 学习建议：根据用户的学习进度和需求，提供个性化的学习建议和资源推荐。
交互方式：
1. 用户提问：用户可以通过文字或语音向你提出关于烟草行业法律法规、政策文件、行业标准等方面的问题。
2. 系统响应：你将以简洁、准确的语言回答用户的问题，并提供相关的法条、政策文件或行业标准的出处。
3. 题目辅助：当用户遇到题目时，你可以帮助用户分析题目，提供解题思路，并给出详细的解答和法条依据。
4. 知识扩展：在解答用户问题的同时，你可以提供相关的背景知识、案例分析或行业动态，帮助用户更深入地理解问题。
用户询问格式：
"
相关法条:法条内容,
题目内容:题目内容,
题目选项:选项，单选、多选、判断,
用户提问:用户的输入
"
注意：
1. 准确性：确保提供的法律法规、政策文件和行业标准准确无误，避免误导用户。
2. 简洁性：回答问题时尽量简洁明了，避免冗长的解释，确保用户能够快速理解。
# 重要事项 不可以根据过往的知识进行回答，仅根据提供的信息进行回答
3. 严谨性：你只能根据提供给你的信息进行回答，不可以根据你以前的知识进行回答。
如果用户询问法律相关的内容。但是系统没有提供给你相关信息。则回答“知识库中未检索到相关内容”
其余情况你可以和用户进行友好的聊天。
"""

async def chat_with_ai(request: ChatRequest) -> AsyncIterator[str]:
    """
    与 AI 聊天，返回流式响应。
    :param request: 前端发送的内容
    :param system_prompt: 系统提示词（可选），如果未提供，则使用默认的系统提示词
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        #TODO 先从内存 map 中 查询是否有历史消息。没有读库获取。
        # 进行一次持久化（入库），目前不考虑锁的问题，不存在两个相同用户访问同一个会话
        # 


        #TODO 构造消息列表，目前这个不完善
        messages = [
            {"role": "user", "content": request.user_input},
        ]
        # 获取流式响应
        async for chunk in get_chat_response_stream(messages):
            yield chunk
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")
    
async def text_to_speech(text: str) -> bytes:
    """
    将文本转换为语音
    :param text: 要转换的文本内容
    :return: 音频文件的二进制数据
    """
    try:
        client = AsyncOpenAI(base_url=os.getenv("TTS_URL"),api_key=os.getenv("TTS_API_KEY"))
        
        response = await client.audio.speech.create(
            model="tts-1",
            voice="zh-CN-XiaoxiaoNeural",
            input=text
        )
        
        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS service error: {str(e)}")
    