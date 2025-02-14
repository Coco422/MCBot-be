from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from models.lg_models import CaseIdResponse, CaseInfoResponse, CaseChatRequest, ForwardAiRequest, ForwardEmbedRequest, GenerateReplyRequest, GenerateExtractIssuesReplyRequest
from services.lg_service import (
    chat_with_llm, 
    get_case_ids_from_db, 
    get_case_info_from_db, 
    get_kb_from_db, 
    generate_reply_by_llm, 
    extract_issues_from_chat, 
    generate_extract_issues_reply_with_kb_by_ai
    )
from tools.embedding_service import embedding_service
from tools import openai_chat
from typing import List

# Create a new router with the /lg prefix
lg_router = APIRouter(prefix="/lg",tags=["LG"])

# --- Endpoint 1: Get case IDs by handler and date ---
@lg_router.get("/caseids", response_model=List[CaseIdResponse])
async def get_case_ids(
    creatby: str = Query(..., description="Work order handler ID"),
    createtime_start: str = Query(..., description="Date (YYYY-MM-DD)"),
    createtime_end: str = Query(..., description="Date (YYYY-MM-DD)"),
):
    try:
        return await get_case_ids_from_db(creatby, createtime_start, createtime_end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 2: Get case info by handler, date, and case ID ---
@lg_router.get("/caseinfo", response_model=CaseInfoResponse)
async def get_case_info(
    creatby: str = Query(..., description="Work order handler ID"),
    createtime_start: str = Query(..., description="Date (YYYY-MM-DD)"),
    createtime_end: str = Query(..., description="Date (YYYY-MM-DD)"),
    caseid: str = Query(..., description="Work order ID"),
):
    try:
        return await get_case_info_from_db(creatby, createtime_start, createtime_end, caseid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@lg_router.post("/chat")
async def chat_train(request: CaseChatRequest):
    """
    SSE 接口，用于
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = chat_with_llm(request),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@lg_router.get("/search_kb")
async def search_kb(text: str = Query(..., description="Search text")):
    """
    搜索知识库
    """
    try:
        return await get_kb_from_db(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@lg_router.post("/generate_current_reply")
async def generate_current_reply(request: GenerateReplyRequest):
    """
    SSE 接口, 生成回复
    针对当前 用户问题以及 历史对话 和 知识库内容 生成回复
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = generate_reply_by_llm(request.chat_history, request.kb_content, request.user_input, request.if_r1),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# endpoit 从聊天记录中提取用户咨询问题列表
@lg_router.post("/extract_issues")
async def extract_issues(request: GenerateReplyRequest):
    """
    从聊天记录中提取用户咨询问题列表
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = extract_issues_from_chat(request.chat_history,request.if_r1),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# endpoit 功能要求：依据提取到的问题，参考坐席回复和知识库，生成参考答案，充实知识库。或结合问答，生成培训案例
@lg_router.post("/generate_extract_issues_reply_by_kb")
async def generate_extract_issues_reply_with_kb(request: GenerateExtractIssuesReplyRequest):
    """
    依据提取到的问题，参考坐席回复和知识库，生成参考答案，充实知识库。或结合问答，生成培训案例
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = generate_extract_issues_reply_with_kb_by_ai(request.chat_history, request.issues, request.if_r1, request.kb_content),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@lg_router.post("/forward_ai")
async def forward_post(request: ForwardAiRequest):
    # 转发 post 请求到 AI 服务 去掉前缀 
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = openai_chat.get_chat_response_stream_langchain(request.messages, 
                                                                     request.system_prompt, 
                                                                     request.model_name, 
                                                                     request.if_r1),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@lg_router.post("/forward_embed")
async def forward_embed_post(request: ForwardEmbedRequest):
        # 转发 post 请求到 embed 服务 去掉前缀 
    try:
        result = await embedding_service.get_embedding(text=request.msg)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))