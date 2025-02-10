from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from models.lg_models import CaseIdResponse, CaseInfoResponse, CaseChatRequest, GenerateReplyRequest
from services.lg_service import chat_with_llm, get_case_ids_from_db, get_case_info_from_db,get_kb_from_db
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

@lg_router.get("/generate_reply")
async def generate_reply(request: GenerateReplyRequest):
    """
    SSE 接口, 生成回复
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(
            content = generate_reply(request),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
