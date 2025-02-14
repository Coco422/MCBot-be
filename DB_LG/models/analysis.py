from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    """
    /api/analysis 接口的响应体模型
    """
    analysis: str  # AI 生成的法律分析内容
    status: str = "success"  # 响应状态