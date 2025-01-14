from psycopg2 import pool
import os
# 数据库连接配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),  # 将端口号转换为整数
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# 创建连接池（可选，提高性能）
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_db_connection():
    """
    获取数据库连接
    """
    try:
        connection = connection_pool.getconn()
        return connection
    except Exception as e:
        raise Exception(f"数据库连接失败: {str(e)}")

def release_db_connection(connection):
    """
    释放数据库连接
    """
    try:
        connection_pool.putconn(connection)
    except Exception as e:
        raise Exception(f"释放数据库连接失败: {str(e)}")