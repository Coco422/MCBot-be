from fastapi import APIRouter, HTTPException
from tools.embedding_service import embedding_service
from tools.openai_chat import get_chat_response_stream_langchain
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import json 
import os

from database.connection import get_db_connection, release_db_connection

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------

# 创建路由器
dev_router = APIRouter(prefix="/dev", tags=["Dev"])

@dev_router.get("/chat_history")
async def get_chat_history():
    """
    获取聊天历史记录
    """
    connection = None
    cursor = None
    try:
        # 获取数据库连接
        connection = get_db_connection()
        cursor = connection.cursor()

        # 执行 SQL 查询
        sql = "SELECT * FROM tobacco.chat_history"
        cursor.execute(sql)

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        columns = [desc[0] for desc in cursor.description]  # 获取列名
        chat_history = [dict(zip(columns, row)) for row in results]

        return {"status": "success", "data": chat_history}

    except Exception as e:
        # 捕获异常并返回错误信息
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

    finally:
        # 关闭游标并释放连接
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)

@dev_router.delete("/clear_chat_history")
async def clear_chat_history():
    """
    清空聊天历史记录
    """
    connection = None
    cursor = None
    try:
        # 获取数据库连接
        connection = get_db_connection()
        cursor = connection.cursor()

        # 执行 SQL 查询
        sql = "TRUNCATE TABLE tobacco.chat_history;"
        cursor.execute(sql)

        # 提交事务
        connection.commit()

        return {"status": "success"}

    except Exception as e:
        # 捕获异常并返回错误信息
        raise HTTPException(status_code=500, detail=f"清空失败: {str(e)}")

    finally:
        # 关闭游标并释放连接
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection)


# 新增接口：获取题目信息 getQues
@dev_router.get("/getQues")
async def get_ques(q_id: int):
    """
    获取题目信息接口
    接收参数: q_id(int)
    返回相应题目信息
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection("lg")
        cursor = connection.cursor()
        sql = "SELECT q_id, q_stem, OPTIONS, q_type, answer, ori_kg_cate, law_content, aimi_quse_5, analysis_qwen32 FROM csm.te_exam_question WHERE q_id = %s"
        cursor.execute(sql, (q_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")
        columns = [desc[0] for desc in cursor.description]
        ques = dict(zip(columns, row))
        return {"status": "success", "data": ques}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection,"lg")


# 新增接口：自由问答接口 chatQusetion
@dev_router.get("/chatQusetion")
async def chat_question(user_question: str):
    """
    自由问答接口
    接收参数: user_question(string)
    实现逻辑：将用户问题通过外部编码接口编码为向量, 然后根据向量查询知识点内容返回给用户
    """
    # 调用外部编码接口将用户问题编码为向量
    embedding = await embedding_service.get_embedding(user_question)

    # 利用向量查询知识点内容
    connection = None
    cursor = None
    try:
        connection = get_db_connection("lg")
        cursor = connection.cursor()
        sql = "SELECT title, content, similarity FROM csm.use_vec_get_top5_medic_kgcont(%s::public.vector)"
        cursor.execute(sql, (embedding,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No knowledge content found")
        columns = [desc[0] for desc in cursor.description]
        knowledge = dict(zip(columns, row))
        return {"status": "success", "data": knowledge}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询知识点失败: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection,"lg")

# 新增接口：生成考卷 geneQusetion
@dev_router.get("/geneQusetion")
async def generate_question_with_kb_by_ai(kb_content: str):
    """
    依据提取到的问题，去数据库生成rag寻找五个参考知识，让AI生成一套考卷。
    :param kb_content: RAG参考内容
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        # 构造消息列表
        messages = []
        
        # 构造系统提示词。任务为参考 用户与客服聊天记录。以及知识点，生成客服接下来的回复
        __system_prompt = f"""
        ## 任务描述：
        你是广东省深圳市医保局的培训老师，负责出题，用于培训和评测新进的政务客服人员，
        请根据给到你的医保知识点(知识点由问题和答案组成)，出8道题目。
        请按考卷方式出题。带格式题号，但是不要question，option等修饰符号
        其中2道判断题，4道单选题，2道多选题。判断题和单选题每题1分，多选题每题2分，合计10分。
        以下是5条参考知识点：
        {kb_content}
        你生成的考题是：
        """
        # 调用外部编码接口将用户问题编码为向量
        embedding = await embedding_service.get_embedding(__system_prompt)
        
        # 利用向量查询知识点内容
        connection = None
        cursor = None
        try:
            connection = get_db_connection("lg")
            cursor = connection.cursor()
            sql = "SELECT title, content, similarity FROM csm.use_vec_get_top5_medic_kgcont(%s::public.vector)"
            cursor.execute(sql, (embedding,))
            rows = cursor.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="No knowledge content found")
            
            # 构建知识点内容
            knowledge_content = "\n".join([f"{row[0]}\n{row[1]}" for row in rows])  #row[0] is title, row[1] is content
            # 构造消息列表
            messages.append({"role": "system", "content": __system_prompt})
            messages.append({"role": "user", "content": knowledge_content})
            
            # 调用模型
            response_generator = get_chat_response_stream_langchain(messages, system_prompt=__system_prompt, model_name=os.getenv("ai_chat_model"))
            return StreamingResponse(response_generator, media_type="text/event-stream")  # Wrap in StreamingResponse

        except json.JSONDecodeError as e:
            logger.error("json 解析失败")
            raise HTTPException(status_code=500, detail="JSON Decode Error") from e
        except Exception as e:
            raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                release_db_connection(connection, "lg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成考题失败: {str(e)}")


# 新增接口：根据分类信息获取题目id getQuesid
@dev_router.get("/getQuesid")
async def get_quesid(q_cate: str):
    """
    获取题目信息接口
    接收参数: q_cate(string)
    返回该类别下的所有题目ID
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection("lg")
        cursor = connection.cursor()
        sql = "SELECT q_id FROM csm.te_exam_question WHERE ori_kg_cate = %s"
        cursor.execute(sql, (q_cate,))
        rows = cursor.fetchall()  # 获取所有行，而不仅仅是一行
        
        if not rows:
            raise HTTPException(status_code=404, detail="No questions found for this category")
        
        # 获取列名
        columns = [desc[0] for desc in cursor.description]
        
        # 将每行转换为字典并添加到列表中
        questions = []
        for row in rows:
            question = dict(zip(columns, row))
            questions.append(question)
        
        return {"status": "success", "data": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            release_db_connection(connection, "lg")