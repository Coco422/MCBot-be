from fastapi import APIRouter, HTTPException

from database.connection import get_db_connection, release_db_connection


# 创建路由器
dev_router = APIRouter(prefix="/dev")

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
