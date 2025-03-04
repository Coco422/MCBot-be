from fastapi import APIRouter, HTTPException
from tools.embedding_service import embedding_service

from database.connection import get_db_connection, release_db_connection


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




            