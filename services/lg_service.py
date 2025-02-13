import json
import os
from typing import AsyncIterator, List, Optional

from fastapi import HTTPException
from models.lg_models import (CaseChatRequest,  
                              CaseInfoResponse,  
                              )
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

        async for chunk in get_chat_response_stream_langchain(messages, system_prompt=__system_prompt, model_name="deepseek-r1:32b-qwen-distill-fp16",if_r1=True):
            yield chunk
    
    except json.JSONDecodeError as e:
        logger.error("json 解析失败")
        pass
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")

async def get_case_ids_from_db(creatby: str, createtime_start: str, createtime_end: str) -> List[str]:
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
    c.calltime,
    c.kg_content                 
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
                    calltime=result[10],
                    kb_content=result[11],
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

async def generate_reply_by_llm(kb_content: List[dict], chat_history: List[dict], user_input: str, if_r1: bool) -> AsyncIterator[str]:
    """
    返回流式AI 生成响应。
    :param kb_content: 知识库内容
    :param chat_history: 聊天记录
    :param user_input: 用户输入
    :param if_r1: 是否开启 R1
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        # 构造消息列表
        messages = []
        # 构造系统提示词。任务为参考 用户与客服聊天记录。以及知识点，生成客服接下来的回复
        __system_prompt = f"""以下是供你参考的知识库内容:
        ```\n{kb_content}\n```
          以下是用户与客服的对话记录:
        ```\n{chat_history}\n```
        ## 任务
        请参考以上内容和接下来的用户输入，生成客服回复（使用中文）"""

        messages.append({"role": "user", "content": user_input})  # 添加当前用户输入
        # 查看是否开启R1 选择不同的模型
        if if_r1:
            __model_name = os.getenv("R1_MODEL_NAME")
        else:
            __model_name = "gpt-4o-mini"
        logger.debug(f"user need to use model: {__model_name}")

        async for chunk in get_chat_response_stream_langchain(messages, model_name=__model_name, system_prompt=__system_prompt):
            yield chunk

    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")
    
async def extract_issues_from_chat(chat_history: List[dict], if_r1: bool) -> AsyncIterator[str]:
    """
    从聊天记录中提取用户咨询问题列表
    :param chat_history: 聊天记录
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        # 构造消息列表
        messages = []
        # 构造系统提示词。任务为参考 用户与客服聊天记录。以及知识点，生成客服接下来的回复
        __system_prompt = """
        ## 任务描述：
你是龙岗区政数局的工单质量监管人员，现在需要对聊天记录总结用户问题。
给到你的数据有聊天记录transcription，聊天记录是客服和群众的通话记录，其中transcription是json数组，每个数组元素中talk值为说话人，分为master客服和slave用户，我们主要对用户问题进行总结，尽可能多得根据用户对话总结出问题，text值是对话内容。
注意，给到的聊天记录中可能存在错别字，请根据场景进行订正并理解。

## 示例对话历史：
```
[{"role" : "assistant", "content" : "您好龙岗区政务服务中心请问有什么可以帮您"}, {"role" : "user", "content" : "你好我预约的那个就是说工伤离职之后不是社保局还有一个月那个补助嘛"}, {"role" : "user", "content" : "那你你们那里办理吗"}, {"role" : "assistant", "content" : "工伤离职领取补助"}, {"role" : "user", "content" : "他不是有一次性那个医疗教育金嘛"}, {"role" : "assistant", "content" : "稍等一下我帮您查询一下"}, {"role" : "user", "content" : "我预约的他是在你们那个政务中心不知道是社保中心还是在社保局问问"}, {"role" : "assistant", "content" : "龙岗区政务服务中心也有社保受理窗口您指您说的是工伤一次性补助吗"}, {"role" : "user", "content" : "不是你别说公章一次性补助那个领过了就说我现在离职之后嘛他公司那个财务嘛离职之后社保局还应该还有一个月那个医疗就业补助金"}, {"role" : "assistant", "content" : "一次性工伤医疗补助金是吗"}, {"role" : "user", "content" : "就业补助金啊对"}, {"role" : "assistant", "content" : "是刚刚跟您说的一次性工伤医疗补助金吗"}, {"role" : "user", "content" : "啊对"}, {"role" : "assistant", "content" : "稍等"}, {"role" : "assistant", "content" : "先生您好抱歉久等了那我这边在这个广东政务服务网上面搜索这个一次性工伤医疗补助金申请它是由人力资源和社会保障局那边去申请的那您这边您是预约了龙岗区政务服务中心吗"}, {"role" : "user", "content" : "啊"}, {"role" : "assistant", "content" : "那那您就按照预约时间到这边来办理社保受理业务"}, {"role" : "user", "content" : "哦你们那边也可以办理是吧"}, {"role" : "assistant", "content" : "这边有社保受理的窗口"}, {"role" : "user", "content" : "哦好行我就怕过来的时候你们那边不办理我先问一下"}, {"role" : "assistant", "content" : "我稍后把一个龙岗区社保站的咨询电话短信发给您您也可以拨打他们社保的电话去进一步咨询一下但是我们这边龙岗区政务服务中心它也有社保受理窗口"}, {"role" : "user", "content" : "哦好谢谢啊"}, {"role" : "assistant", "content" : "嗯不客气稍后短信发到您手机尾号六五七五哈"}, {"role" : "assistant", "content" : "您还有其他问题吗"}, {"role" : "user", "content" : "没有就这个问题我约的是下午我先问一下"}, {"role" : "assistant", "content" : "嗯好的"}]
```
## 示例回答（有序列表，美观输出，每一条后面换行）:
	1.	工伤离职后，社保局是否还会发放一个月的补助金？
	2.	该补助金是否可以在龙岗区政务服务中心办理？
	3.	关注的补助金类型是“一次性医疗就业补助金”，且已领取过其他补助。
	4.	已预约龙岗区政务服务中心，该中心是否能处理此问题？
	5.	龙岗区政务服务中心是否设有社保受理窗口，可办理相关业务？
"""
        
        # 处理chat_history。帮某个jackass擦屁股，先把 chat_history从 list[dict] 转为字符串
        json_string = json.dumps(chat_history, ensure_ascii=False)  # ensure_ascii=False 以保留中文字符

        __fix_chat_history = json_string.replace("slave", "user").replace("master", "assistant").replace("talk", "role").replace("text", "content")

        messages.append({"role": "user", "content": f"""
## 真实对话历史：
``` 
{__fix_chat_history}
```
## 开始: (最终输出仅完成任务即提取问题即可，不要在思考后输出无关内容)"""})  # 添加当前用户输入
        # 查看是否开启R1 选择不同的模型
        if if_r1:
            __model_name = os.getenv("R1_MODEL_NAME")
        else:
            __model_name = "gpt-4o-mini"
        logger.debug(f"user need to use model: {__model_name}")

        async for chunk in get_chat_response_stream_langchain(messages, model_name=__model_name, system_prompt=__system_prompt):
            yield chunk

    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")

async def generate_extract_issues_reply_with_kb_by_ai(chat_history: List[dict], issues: List[str], if_r1: bool, kb_content:str) -> AsyncIterator[str]:
    """
    依据提取到的问题，参考坐席回复和知识库，生成参考答案，充实知识库。或结合问答，生成培训案例
    :param chat_history: 聊天记录
    :param issues: 总结出来的问题
    :param if_r1: 是否开启 R1
    :param kb_content: 知识库内容
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        # 构造消息列表
        messages = []
        # 构造系统提示词。任务为参考 用户与客服聊天记录。以及知识点，生成客服接下来的回复
        __system_prompt = """
        ## 任务描述：
        根据输入的内容
        1. 对话历史（这是由 ASR 转写的，所以会有文字错乱）
        2. 总结出来的用户咨询的问题列表
        3. 知识库内容
        给出 针对每个问题的回答（以客服的口吻）。以美观的 json 结构输出。包括缩进换行等
        ## 示例结构
        {
            "response":
            [
            {"question":"港澳通行证签证是否可以在龙岗政务中心办理？",
            "answer":"港澳通行证签证不在龙岗政务服务中心办理，请前往出入境大厅进行办理。如需查询更多信息，可拨打咨询电话83991869或联系区行政服务大厅获取具体指引。"
            }
            ]
        } 
        """

        json_string = json.dumps(chat_history, ensure_ascii=False)  # ensure_ascii=False 以保留中文字符

        __fix_chat_history = json_string.replace("slave", "user").replace("master", "assistant").replace("talk", "role").replace("text", "content")

        messages.append({"role": "user", "content": f"""
## 真实对话历史：
```
{__fix_chat_history}
```
## 提取的问题列表:
```
{issues}
```
## 知识库内容:
```
{kb_content}
```
## 开始: (最终输出仅完成任务即可)以美观的 json 结构输出简体中文。包括缩进换行等
"""})   # 添加当前用户输入
        # 查看是否开启R1 选择不同的模型
        if if_r1:
            __model_name = os.getenv("R1_MODEL_NAME")
        else:
            __model_name = "gpt-4o-mini"
        logger.debug(f"user need to use model: {__model_name}")

        async for chunk in get_chat_response_stream_langchain(messages, model_name=__model_name, system_prompt=__system_prompt):
            yield chunk

    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")