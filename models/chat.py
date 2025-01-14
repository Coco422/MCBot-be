from pydantic import BaseModel
from typing import Optional, List

# 定义请求体模型
class ChatRequest(BaseModel):
    """
    /chat/train 接口的请求体模型
    """
    user_input: str  # 用户输入的内容
    system_prompt: Optional[str] = None  # 系统提示词（可选）
    lows: Optional[List[str]] = None  # 相关法条（可选）
    question: Optional[str] = None  # 题目内容（可选）
    options: Optional[List[str]] = None  # 题目选项（可选）
    
# 定义响应模型
class ChatResponse(BaseModel):
    response: str
    status: str = "success"
