from psycopg2 import pool
import os

# 数据库连接配置
DB_CONFIGS = {
    "dev": {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    },
    "prod": {
        "host": os.getenv("Pord_DB_HOST"),
        "port": int(os.getenv("Pord_DB_PORT")),
        "user": os.getenv("Pord_DB_USER"),
        "password": os.getenv("Pord_DB_PASSWORD"),
        "database": os.getenv("Pord_DB_NAME"),
    }
}

# 创建连接池
connection_pools = {
    "dev": pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **DB_CONFIGS["dev"]
    ),
    "prod": pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **DB_CONFIGS["prod"]
    )
}

def get_db_connection(db_type="dev"):
    """
    获取数据库连接
    :param db_type: 数据库类型，可选 'dev' 或 'prod'
    :return: 数据库连接对象
    """
    if db_type not in connection_pools:
        raise ValueError(f"无效的数据库类型: {db_type}")
    
    try:
        connection = connection_pools[db_type].getconn()
        return connection
    except Exception as e:
        raise Exception(f"数据库连接失败: {str(e)}")

def release_db_connection(connection, db_type="dev"):
    """
    释放数据库连接
    :param connection: 要释放的数据库连接
    :param db_type: 数据库类型，可选 'dev' 或 'prod'
    """
    if db_type not in connection_pools:
        raise ValueError(f"无效的数据库类型: {db_type}")
    
    try:
        connection_pools[db_type].putconn(connection)
    except Exception as e:
        raise Exception(f"释放数据库连接失败: {str(e)}")