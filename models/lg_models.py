import datetime
from pydantic import BaseModel,Field
from typing import Optional, List, Any

# --- Pydantic Models ---
class CaseIdResponse(BaseModel):
    caseid: str

class CaseInfoResponse(BaseModel):
    """
    工单信息响应模型
    """
    caseid: str = Field(..., description="工单ID")
    problemdescription: str = Field(..., description="问题描述")
    problemreply: str = Field(..., description="问题回复")
    think: Optional[Any] = Field(None, description="推理部分，可以为空")
    ai_comment: Optional[Any] = Field(None, description="AI 评论部分，可以为空")
    transcription: Optional[Any] = Field(None, description="语音转录数据")
    score: Any = Field(..., description="客服回答质量评分细则")
    fit: Any = Field(..., description="小结准确度评分细则")
    callee: Optional[Any] = Field(None, description="被叫")
    caller: str = Field(..., description="主叫")
    calltime: Optional[Any] = Field(None, description="通话时间")

class CaseChatRequest(BaseModel):
    """
    /lg/chat 接口的请求体模型
    """
    user_input: str = Field(..., description="用户输入的内容")
    chat_type: Optional[int] = Field(0, description="对话类型 0: 一般对话 1: 知识库问答对话 2: 评价")
    if_kb: Optional[bool] = Field(False, description="是否开启知识库查询")

    case_id: Optional[str] = Field(None, description="工单 ID")
    case_date_begin: Optional[str] = Field(None, description="工单日期 开始")
    case_date_end: Optional[str] = Field(None, description="工单日期 结束")
    case_create_by: Optional[str] = Field(None, description="工单创建人")
    case_problem_description: Optional[str] = Field(None, description="工单问题描述")


    chat_id: Optional[str] = Field(
        'f47e1111-1111-1111-1111-111111111111',
        description="必须传入对话 uuid。否则存入默认 uuid 为测试用 id 会查不到历史记录"
    )

class GenerateReplyRequest(BaseModel):
    """
    /lg/generate_reply 接口的请求体模型
    """
    user_input: str = Field(..., description="用户输入的内容")
    # 查询到的知识库内容
    kb_content: Optional[str] = Field(None, description="知识库内容")

