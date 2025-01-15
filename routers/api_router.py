from fastapi import APIRouter, Query, HTTPException, Response
from fastapi.responses import StreamingResponse
from services.tobacco_study import get_random_question, get_law_slices_by_question_id, get_analysis_by_question_id
from services.chat_service import chat_with_ai,text_to_speech,create_chat_id
from models.question import Question
from models.law import LawSlice
from models.chat import ChatRequest
from models.analysis import AnalysisResponse
from models.common import ChatIdResponse, TTSRequest


# 创建路由器
api_router = APIRouter(prefix="/api")

# 随机题目接口
@api_router.get("/randomquestion", response_model=Question)
async def random_question():
    try:
        return get_random_question()
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))

# 题目对应法条切片接口
@api_router.get("/lows", response_model=list[LawSlice])
async def law_slices(questionid: int = Query(..., description="题目ID")):
    try:
        return get_law_slices_by_question_id(questionid)
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))
    
@api_router.post("/chat/train")
async def chat_train(request: ChatRequest):
    """
    SSE 接口，用于学习时与 AI 聊天。
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(content = chat_with_ai(request),media_type="text/event-stream",)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@api_router.get("/analysis", response_model=AnalysisResponse)
async def analysis(questionid: int = Query(..., description="题目ID")):
    """
    获取 AI 生成的法律分析内容
    """
    try:
        return get_analysis_by_question_id(questionid)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))

@api_router.get("/chatid", response_model=ChatIdResponse)
async def generate_chat_id():
    """
    生成一个唯一的 chat_id 并返回
    """
    try:
        # 生成唯一的 chat_id
        chat_id = create_chat_id()
        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@api_router.post("/tts")
async def generate_tts(request: TTSRequest):
    """
    生成文字转语音
    """
    try:
        #TODO 暂未完成自定义说话人等

        audio_data = await text_to_speech(request.tts_text)
        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
