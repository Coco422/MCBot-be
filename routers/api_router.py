import asyncio
from fastapi import APIRouter, Query, HTTPException, Response, File, UploadFile
# from fastapi.responses import StreamingResponse
from starlette.responses import StreamingResponse
from services.tobacco_study import get_random_question, get_law_slices_by_question_id, get_analysis_by_question_id
from services.chat_service import chat_with_ai, chat_with_ai_analysis
from services.chat_manage import create_chat_id, get_chat_id_list_from_db, get_chathis_by_id
from services.voice_service import text_to_speech, speech_to_text, clone_voice
from models.question import Question
from models.law import LawSlice
from models.chat import ChatAnalysisRequest, ChatTrainRequest, ChatHistoryResponse
from models.analysis import AnalysisResponse
from models.common import ChatIdResponse, TTSRequest, VoiceCloneRequest, ChatIdListResponse
from typing import AsyncIterator

# 创建路由器
api_router = APIRouter(prefix="/api")

# 随机题目接口
@api_router.get("/randomquestion", response_model=Question)
async def random_question():
    try:
        return get_random_question(999999)
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))

# 返回指定题目接口
@api_router.get("/query_question_by_id", response_model=Question)
async def random_question(questionid: int = Query(..., description="题目ID")):
    try:
        return get_random_question(questionid)
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))

# 题目对应法条切片接口
@api_router.get("/lows", response_model=list[LawSlice])
async def law_slices(questionid: int = Query(..., description="题目ID")):
    try:
        return get_law_slices_by_question_id(questionid)
    except Exception as e:
        raise HTTPException(status_code=5000, detail=str(e))

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
async def generate_chat_id(user_id: str = Query(..., description="用户的凭证")):
    """
    生成一个唯一的 chat_id 并返回
    """
    try:
        #TODO 需要验证用户 id
        # 生成唯一的 chat_id
        chat_id = create_chat_id(user_id)
        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@api_router.get("/chatid_list", response_model=ChatIdListResponse)
async def get_chat_id_list_by_user_id(user_id: str = Query(..., description="用户的凭证")):
    """
    返回当前用户的所有 chat_id 的 list
    """
    try:
        #TODO 需要验证用户 id
        # 生成唯一的 chat_id
        chat_id_list = get_chat_id_list_from_db(user_id)
        return {"chat_id_list": chat_id_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/chat_byid", response_model=ChatHistoryResponse)
async def get_chat_by_id(chat_id: str = Query(..., description="对话的 chat_id")):
    """
    用于获取指定 chat_id 的对话历史
    """
    try:
        #TODO 逻辑未鉴权
        messages = get_chathis_by_id(chat_id)
        print(f"chat_id: {chat_id}, messages: {messages}")
        return {"chat_id":chat_id,"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/asr", summary="语音转文本", description="上传音频文件并返回识别后的文本")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # 检查文件类型
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="仅支持音频文件")

        # 读取文件内容
        file_content = await file.read()

        # 调用 services 模块中的 speech_to_text 函数
        text_result = await speech_to_text(file_content, file.filename)

        # 返回识别结果
        return {"text": text_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/clone-voice",  summary="克隆用户音色生成对应音频")
async def clone_voice_endpoint(request: VoiceCloneRequest):
    """
    上传用户录音文件、自定义名称和参考文本，用于预置音色。
    - **custom_name**: Optional[str] = "MCBotDEMO"用户自定义的音频名称
    - **reference_text**: Optional[str]参考音频的文字内容
    - **base64_audio**: base64 Optional[str]编码的音频数据
    - **tts_text**: str # 目标生成的文字
    """
    try:
        audio_data = await clone_voice(request)
        return Response(content=audio_data, media_type="audio/mpeg")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/chat/train")
async def chat_train(request: ChatTrainRequest):
    """
    SSE 接口，用于学习时与 AI 聊天。
    """
    try:
        # 返回 StreamingResponse
        return StreamingResponse(content = chat_with_ai(request),media_type="text/event-stream",)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/chat/analysis")
async def chat_analysis(request: ChatAnalysisRequest):
    """
    SSE 接口，用于分析时与 AI 聊天。
    """
    try:
        return StreamingResponse(
            content=chat_with_ai_analysis(request),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/tts")
async def generate_tts(request: TTSRequest):
    """
    生成文字转语音

    - **tts_text**: 需要转换为语音的文本
    - **返回**: 语音数据 (audio/mpeg)
    """
    try:
        #TODO 暂未完成自定义说话人等

        audio_data = await text_to_speech(request.tts_text)
        return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
