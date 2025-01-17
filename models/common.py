from pydantic import BaseModel, Field
from fastapi import UploadFile
from typing import Optional
# 定义响应模型
class ChatIdResponse(BaseModel):
    chat_id: str

class ChatIdListResponse(BaseModel):
    chat_id_list: list = Field(...,description="返回当前用户拥有的chat_id list")

class TTSRequest(BaseModel):
    tts_text: str = Field(
        ...,
        description="需要转换为语音的文本内容。",
        example="你好，欢迎使用文字转语音服务。"
    )

class VoiceCloneRequest(BaseModel):
    custom_name: Optional[str] = "MCBotDEMO"  # 用户自定义的音频名称
    reference_text: Optional[str] = None  # 参考音频的文字内容
    base64_audio: Optional[str] = None  # base64 编码的音频数据
    tts_text: str # 目标生成的文字

