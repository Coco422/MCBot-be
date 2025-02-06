from pydantic import BaseModel,Field
from typing import Optional, List

class ChatTrainRequest(BaseModel):
    """
    /chat/train 接口的请求体模型
    """
    user_input: str = Field(..., description="用户输入的内容")
    if_kb: Optional[bool] = Field(False, description="是否开启知识库查询")
    if_stream: Optional[bool] = Field(True, description="是否开启流式返回")
    question_id: Optional[int] = Field(None, description="当前询问问题 id")
    chat_id: Optional[str] = Field(
        'f47e82a1-1878-453f-81e9-e9641773abd5',
        description="必须传入对话 uuid。否则存入默认 uuid 为测试用 id 会查不到历史记录"
    )
    system_prompt: Optional[str] = Field(None, description="系统提示词（可选）")
    lows: Optional[List[str]] = Field(None, description="相关法条（可选）")
    question: Optional[str] = Field(None, description="题目内容（可选）")
    options: Optional[List[str]] = Field(None, description="题目选项（可选）")

class ChatAnalysisRequest(BaseModel):
    """
    /chat/analysis 接口的请求体模型
    """
    user_input: str = Field(..., description="用户输入的内容")
    chat_id: Optional[str] = Field(
        'f47e82a1-1878-453f-81e9-e9641773abd6',
        description="必须传入对话 uuid。否则存入默认 uuid 为测试用 id 会查不到历史记录"
    )
    database_id: Optional[str]= Field(
        description="可选数据库的 标识"
    )

# 定义响应模型
class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# 聊天历史模型
class ChatHistoryResponse(BaseModel):
    chat_id: str = Field(..., description="对话的唯一标识")
    messages: Optional[List[dict]] = Field(None, description="对话历史记录")