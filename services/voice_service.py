import requests
from models.common import VoiceCloneRequest
from fastapi import HTTPException
import os
import aiohttp
from openai import AsyncOpenAI

async def text_to_speech(tts_text: str) -> bytes:
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
            input=tts_text
        )
        
        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS service error: {str(e)}")

async def speech_to_text(file_content: bytes, filename: str) -> str:
    # print("1. 开始调用 speech_to_text 函数")
    # print(f"2. 文件名: {filename}, 文件大小: {len(file_content)} 字节")

    url = os.getenv("asr_url")
    key = os.getenv("siliconflow_key")
    headers = {
        "Authorization": "Bearer "+key,
    }

    # print("3. 构建 multipart/form-data 请求体")
    data = aiohttp.FormData()
    data.add_field('file', file_content, filename=filename, content_type='audio/wav')
    data.add_field('model', os.getenv("asr_model"))

    # print("4. 准备发起 API 请求")
    # print(f"5. 请求 URL: {url}")
    # print(f"6. 请求头: {headers}")
    # print(f"7. 请求体: {data}")

    try:
        # print("8. 创建 aiohttp.ClientSession")
        async with aiohttp.ClientSession() as session:
            # print("9. 发起 POST 请求")
            async with session.post(url, headers=headers, data=data) as response:
                # print(f"10. 请求完成，状态码: {response.status}")

                if response.status == 200:
                    # print("11. 请求成功，解析响应")
                    result = await response.json()
                    # print(f"12. 响应内容: {result}")
                    return result.get("text", "")
                else:
                    # print("13. 请求失败，打印错误信息")
                    error_detail = await response.text()
                    # print(f"14. 错误详情: {error_detail}")
                    raise HTTPException(status_code=response.status, detail=f"API 请求失败: {error_detail}")

    except aiohttp.ClientError as e:
        # print("15. 捕获到 aiohttp.ClientError 异常")
        # print(f"16. 异常详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")

    except Exception as e:
        # print("17. 捕获到未知异常")
        # print(f"18. 异常详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"未知错误: {str(e)}")

async def clone_voice(request: VoiceCloneRequest) -> bytes:
    try:
        if request.base64_audio:
            # 官方 API 的 URL 和 headers
            UPLOAD_AUDIO_URL = "https://api.siliconflow.cn/v1/uploads/audio/voice"
            API_KEY = os.getenv("siliconflow_key")  # 替换为你的 API Key
            HEADERS = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # 构建请求体
            data = {
                "model": "FunAudioLLM/CosyVoice2-0.5B",  # 模型名称
                "customName": request.custom_name,  # 用户自定义的音频名称
                "audio": f"data:audio/wav;base64,{request.base64_audio}",  # base64 编码的音频
                "text": request.reference_text  # 参考音频的文字内容
            }

            # 调用siliconflow API
            response = requests.post(UPLOAD_AUDIO_URL, headers=HEADERS, json=data)

            # 检查响应状态码
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json())
            
            # 解析响应数据
            data = response.json()
            voice_id = data.get("uri", "FunAudioLLM/CosyVoice2-0.5B:alex")

        # 初始化 AsyncOpenAI 客户端
        client = AsyncOpenAI(base_url=os.getenv("siliconflow_base_url"), api_key=os.getenv("siliconflow_key"))

        # 调用 OpenAI 的语音生成 API
        response = await client.audio.speech.create(
            model="FunAudioLLM/CosyVoice2-0.5B",
            voice=voice_id,
            input=request.tts_text
        )

        return response.content
    except Exception as e:
        # 打印异常信息
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))