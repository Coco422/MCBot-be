import json
from typing import AsyncIterator, List, Optional

from fastapi import HTTPException
from models.lg_models import CaseChatRequest, CaseIdResponse, CaseInfoResponse, GenerateReplyRequest
from database.connection import get_db_connection, release_db_connection
from tools.embedding_service import embedding_service


# ----------配置日志-------------
from tools.openai_chat import get_chat_response_stream_langchain
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------



async def chat_with_llm(request: CaseChatRequest) -> AsyncIterator[str]:
    """
    与 AI 聊天，返回流式响应。
    :param request: 前端发送的内容
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    connection = None
    try:

        # 构建系统提示词 先从数据库获取 case info
        """
        request 中包含    case_id: Optional[str] = Field(None, description="工单 ID")
    case_date_begin: Optional[str] = Field(None, description="工单日期 开始")
    case_date_end: Optional[str] = Field(None, description="工单日期 结束")
    case_create_by: Optional[str] = Field(None, description="工单创建人")
    根据这些信息从数据库获取 case info
        """
        if request.case_id:
            case_info = await get_case_info_from_db(
                creatby=request.case_create_by,
                createtime_start=request.case_date_begin,
                createtime_end=request.case_date_end,
                caseid=request.case_id
            )
            __system_prompt = f"以下是供你参考的本次工单个案的信息:\n 工单问题总结描述: {case_info.problemdescription} \n 工单问题总结回复: {case_info.problemreply} \n AI评价: {case_info.ai_comment}"
        else:
            __system_prompt = "用户未提供工单信息"


        # 判断是否开启 RAG
        if request.if_kb:
            finally_input = request.user_input + " [RAG]"
        else:
            finally_input = request.user_input
          
        # 构造消息列表
        messages = []
        messages.append({"role": "user", "content": finally_input})  # 添加当前用户输入

        async for chunk in get_chat_response_stream_langchain(messages, system_prompt=__system_prompt, model_name="deepseek-r1:32b-qwen-distill-q8_0",if_r1=True):
            yield chunk
    
    except json.JSONDecodeError as e:
        logger.error("json 解析失败")
        pass
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")

async def get_case_ids_from_db(creatby: str, createtime_start: str, createtime_end: str) -> List[CaseIdResponse]:
    connection = None
    try:
        connection = get_db_connection(db_type="lg")
        with connection.cursor() as cursor:
            sql = f"""
                SELECT 
                    c.caseid
                FROM 
                    csm.ta_wf_caseinfo c
                WHERE 
                    c.creatby = '{creatby}'
                    AND c.createtime >= '{createtime_start} 01:00:01.100'
                    AND c.createtime <= '{createtime_end} 23:59:59.100'
                """
            cursor.execute(sql)
            results = cursor.fetchall()
            return [{"caseid": result[0]} for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            release_db_connection(connection, db_type="lg")

async def get_case_info_from_db(
    creatby: str, createtime_start: str, createtime_end: str, caseid: str
) -> CaseInfoResponse:
    connection = None
    try:
        connection = get_db_connection(db_type="lg")
        with connection.cursor() as cursor:
            sql = f"""
SELECT
	c.caseid,
    c.problemdescription,   
    c.problemreply,
    CASE
        WHEN POSITION('<think>' IN c.response) > 0 AND POSITION('</think>' IN c.response) > 0
        THEN TRIM(SUBSTRING(
            c.response
            FROM POSITION('<think>' IN c.response)+ 7
            FOR GREATEST(POSITION('</think>' IN c.response) - POSITION('<think>' IN c.response) - 7, 0)
        ))
    END AS think,
		CASE
        WHEN POSITION('</think>' IN c.response) > 0
        THEN TRIM(SUBSTRING(
            c.response
            FROM POSITION('</think>' IN c.response)+8
            FOR GREATEST(POSITION('</think>' IN c.response) , 0)
        ))
    END AS ai_comment,
		 (SELECT 
        json_agg(json_build_object('talk', asr.talk, 'text', asr.text) ORDER BY asr.createtime)
    FROM csm.te_asr_data asr
    WHERE asr.callid = c.callid) AS transcription,
		c.score, 
		c.fit,
    c.callee,                          
    c.caller,                          
    c.calltime                       
FROM
    csm.ta_wf_caseinfo c
WHERE
    c.creatby = '{creatby}'
    AND c.createtime BETWEEN '{createtime_start} 01:00:01.100' AND '{createtime_end} 23:59:59.100'
    AND c.caseid = '{caseid}';
                """
            cursor.execute(sql)
            result = cursor.fetchone()
            # print(result)
            if result:
                return CaseInfoResponse(
                    caseid=result[0],
                    problemdescription=result[1],
                    problemreply=result[2],
                    think=result[3],
                    ai_comment=result[4],
                    transcription=result[5],
                    score=result[6],
                    fit=result[7],
                    callee=result[8],
                    caller=result[9],
                    calltime=result[10]
                )
            else:
                raise HTTPException(status_code=404, detail="Case not found")
    except Exception as e:
        logger.error(f"查询数据库失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            release_db_connection(connection, db_type="lg")

async def get_kb_from_db(text: str) -> Optional[str]:
    """Perform RAG search using embedding service"""
    # Get embedding for the question
    embedding = await embedding_service.get_embedding(text)
    
    # Search for similar content in database
    results = await embedding_service.lg_search_kb_by_chat(embedding)
    
    return results

async def generate_reply(request: GenerateReplyRequest):
    """
    返回流式AI 生成响应。
    :param request: 前端发送的内容
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    connection = None
    try:
        # 构造消息列表
        messages = []
        # 构造系统提示词。任务为参考 用户与客服聊天记录。以及知识点，生成客服接下来的回复
        __system_prompt = f"以下是供你参考的知识库内容:\n {request.kb_content}"

        messages.append({"role": "user", "content": request.user_input})  # 添加当前用户输入
        
        async for chunk in get_chat_response_stream_langchain(messages, model_name="deepseek-r1:32b-qwen-distill-q8_0", system_prompt=__system_prompt):
            yield chunk

    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")