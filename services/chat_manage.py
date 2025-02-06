import json
from database.connection import get_db_connection, release_db_connection
from services.chat_utils import generate_title
import uuid
from psycopg2.extras import Json

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------

# 内存中的对话历史
CHAT_HISTORY_MAP = {}

def create_chat_id(user_id:str):
    """生成唯一的 chat_id"""
    generated_uuid = str(uuid.uuid4())
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO tobacco.chat_history (chat_id, user_id)
        VALUES (%s, %s);
        """
        cursor.execute(query, (generated_uuid, user_id))
        conn.commit()
    except Exception as e:
        logger.error(f"创建chat_id失败: {e}")
    finally:
        if conn:
            release_db_connection(conn)
    return generated_uuid

def save_chat_to_db(chat_id, messages):
    """将对话历史保存到 PostgreSQL 数据库"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO tobacco.chat_history (chat_id, messages)
        VALUES (%s, %s)
        ON CONFLICT (chat_id) DO UPDATE
        SET messages = EXCLUDED.messages, updated_at = CURRENT_TIMESTAMP;
        """
        cursor.execute(query, (chat_id, Json(messages)))
        conn.commit()
    except Exception as e:
        logger.error(f"数据库保存失败: {e}")
    finally:
        if conn:
            release_db_connection(conn)

def load_chat_from_db(chat_id):
    """从 PostgreSQL 数据库加载对话历史"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT messages FROM tobacco.chat_history WHERE chat_id = %s;"
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()
        return result[0] if result else []
    except Exception as e:
        logger.error(f"数据库加载失败: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)

def get_chat_history(chat_id):
    """获取对话历史（优先从内存中获取，内存中没有则从数据库加载）"""
        # Initialize chat history structure if it doesn't exist
    if chat_id not in CHAT_HISTORY_MAP:
        CHAT_HISTORY_MAP[chat_id] = {
            "history": [],
            "title": None
        }

    # Return from memory if exists
    if CHAT_HISTORY_MAP[chat_id]["history"]:
        return CHAT_HISTORY_MAP[chat_id]["history"]
    
    messages = load_chat_from_db(chat_id)
    if messages:
        try:
            messages_json = json.loads(messages)
            CHAT_HISTORY_MAP[chat_id]["history"] = messages_json["history"]
            return CHAT_HISTORY_MAP[chat_id]["history"]
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse chat history: {e}")
            return []
    
    return CHAT_HISTORY_MAP[chat_id]["history"]  # Return empty list if no history found

def get_chat_id_list_from_db(user_id:str)->list:
    """从数据库检索 user_id 所包含的 chat_id"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT chat_id FROM tobacco.chat_history
        WHERE user_id = %s
        ORDER BY created_at DESC;
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        return [row[0] for row in results] if results else []
    except Exception as e:
        logger.error(f"获取chat_id列表失败: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)

async def add_message_to_chat(chat_id, role, content):
    """向对话历史中添加消息"""
    if chat_id not in CHAT_HISTORY_MAP:
        CHAT_HISTORY_MAP[chat_id] = {
            "history": [],  # 存储对话记录
            "title": None   # 初始默认为空
        }
    CHAT_HISTORY_MAP[chat_id]["history"].append({"role": role, "content": content})
    # 判断对话历史记录中是否有标题title 存在
    has_title = CHAT_HISTORY_MAP.get(chat_id, {}).get("title") is not None
    if not has_title:
        CHAT_HISTORY_MAP[chat_id]["title"] = await generate_title(CHAT_HISTORY_MAP[chat_id])
    # 同步到数据库
    save_chat_to_db(chat_id, CHAT_HISTORY_MAP[chat_id])

def get_chathis_by_id(chat_id):
    """根据 chat_id 从数据库获取对话历史"""
    return load_chat_from_db(chat_id)
