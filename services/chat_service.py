import time
from fastapi import HTTPException

from utils.utils import deprecated
from utils.openai_chat import get_chat_response_stream_langchain
from services.tobacco_study import get_random_question, get_law_slices_by_question_id
from utils.embedding_service import embedding_service
from models.question import Question
from models.law import LawSlice
from database.connection import get_db_connection, release_db_connection

from typing import AsyncIterator, List
from models.chat import ChatRequest
import uuid
import json
from psycopg2.extras import Json

# ----------配置日志-------------
from utils.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------

# 内存中的对话历史
chat_history_map = {}

# 默认的系统提示词
DEFAULT_SYSTEM_PROMPT = """\
版本:v0.0.1
开发者:Ray
所属组织:MCKJ

角色设定：
你是一位专业的烟草培训系统学习助手，专门为用户提供烟草行业相关的法律法规知识、解答用户在学习过程中遇到的疑问，并辅助用户完成相关题目。
你具备丰富的烟草行业知识，熟悉国内外烟草行业的法律法规、政策文件以及行业标准。
你的任务是帮助用户更好地理解和掌握烟草行业的相关知识，提升用户的学习效率和专业水平。

主要功能：
1. 法律法规查询：根据用户的需求，快速查询并解释烟草行业相关的法律法规、政策文件、行业标准等。
2. 题目解答：辅助用户解答烟草行业相关的题目，提供详细的解析和法条依据。
3. 知识扩展：在用户提问的基础上，提供相关的背景知识、案例分析或行业动态，帮助用户更全面地理解问题。
4. 学习建议：根据用户的学习进度和需求，提供个性化的学习建议和资源推荐。

交互方式：
1. 用户提问：用户可以通过文字或语音向你提出关于烟草行业法律法规、政策文件、行业标准等方面的问题。
2. 系统响应：你将以简洁、准确的语言回答用户的问题，并提供相关的法条、政策文件或行业标准的出处。
3. 题目辅助：当用户遇到题目时，你可以帮助用户分析题目，提供解题思路，并给出详细的解答和法条依据。
4. 知识扩展：在解答用户问题的同时，你可以提供相关的背景知识、案例分析或行业动态，帮助用户更深入地理解问题。

用户给到你的信息格式：
"
相关文档:
相关文档 
法律ID: 
法律名称: 
章节: 
文章内容: 
相似度: 

题目:题目内容,
类型:单选、多选、判断,
选项:选项,
正确答案:答案,

用户提问:用户的输入
"
注意：
1. 准确性：确保提供的法律法规、政策文件和行业标准准确无误，避免误导用户。
2. 简洁性：回答问题时尽量简洁明了，避免冗长的解释，确保用户能够快速理解。
# 重要事项 不可以根据过往的知识进行回答，仅根据提供的信息进行回答
3. 严谨性：你只能根据提供给你的信息进行回答，不可以根据你以前的知识进行回答。
如果用户询问法律相关的内容。但是系统没有提供给你相关信息。则回答“知识库中未检索到相关内容”
其余情况你可以和用户进行友好的聊天。
"""

def create_chat_id():
    """生成唯一的 chat_id"""
    return str(uuid.uuid4())

def save_to_db(chat_id, messages):
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

def load_from_db(chat_id):
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
    if chat_id in chat_history_map:
        return chat_history_map[chat_id]
    else:
        messages = load_from_db(chat_id)
        if messages:
            chat_history_map[chat_id] = messages
        return messages

def get_chat_id_from_db(user_id):
    #TODO
    pass

def add_message_to_chat(chat_id, role, content):
    """向对话历史中添加消息"""
    if chat_id not in chat_history_map:
        chat_history_map[chat_id] = []
    chat_history_map[chat_id].append({"role": role, "content": content})
    # 同步到数据库
    save_to_db(chat_id, chat_history_map[chat_id])

async def rag_search(question: str) -> List[dict]:
    """Perform RAG search using embedding service"""
    # Get embedding for the question
    embedding = await embedding_service.get_embedding(question)
    
    # Search for similar content in database
    results = await embedding_service.search_similar(embedding)
    
    return results

@deprecated
def format_to_markdown(law_slices: List[LawSlice]) -> str:
    markdown_str = ""
    for law in law_slices:
        markdown_str += f"### 法律名称: {law.law_name}\n"
        markdown_str += f"- **章节**: {law.chapter}\n"
        markdown_str += f"- **条款内容**: {law.article_content}\n"
        markdown_str += f"- **相似度**: {law.similarity:.2f}\n\n"
    return markdown_str

async def chat_with_ai(request: ChatRequest) -> AsyncIterator[str]:
    """
    与 AI 聊天，返回流式响应。
    :param request: 前端发送的内容
    :param system_prompt: 系统提示词（可选），如果未提供，则使用默认的系统提示词
    :return: 返回一个异步迭代器，每次迭代返回一个聊天结果的片段
    """
    try:
        # 获取 chat_id
        chat_id = request.chat_id

        # 判断是否开启 RAG
        if request.if_kb:

            # 先获取用户当前的题目信息
            # 根据id 查询题目信息
            question_option_info_full = get_random_question(request.question_id)
            # 构建 RAG 用的 题目和选项
            question_option = f"q:{question_option_info_full.q_stem};\noptions:{question_option_info_full.options}"
            # 调用RAG搜索
            rag_question_low_results = await rag_search(question_option)
            # 格式化RAG结果
            rag_context = "\n".join(
                f"相关文档 {i+1}:\n"
                f"法律ID: {result['law_id']}\n"
                f"法律名称: {result['law_name']}\n"
                f"章节: {result['chapter']}\n"
                f"文章内容: {result['article_content']}\n"
                f"相似度: {result['similarity']:.2f}\n"
                for i, result in enumerate(rag_question_low_results)
            )
            
            user_input_with_kb = f"""
相关文档:
{rag_context}

用户当前查看题目信息:
题目:{question_option_info_full.q_stem}\n
类型:{question_option_info_full.q_type}\n
选项:{question_option_info_full.options}\n
正确答案:{question_option_info_full.answer}

用户提问:
{request.user_input}
"""
            finally_input = user_input_with_kb
        else:
            finally_input = request.user_input
        # 避免 token 浪费，这里历史记录只存用户的问题，对对话影响不是很大。但是这里后续要改进 TODO
        add_message_to_chat(chat_id, "user", request.user_input)
        # 加载历史消息
        history = get_chat_history(chat_id)

        # 构造消息列表
        messages = history.copy()  # 复制历史消息
        messages.append({"role": "user", "content": finally_input})  # 添加当前用户输入

        async for chunk in get_chat_response_stream_langchain(messages,system_prompt=DEFAULT_SYSTEM_PROMPT):
            yield chunk
    
        full_response = chunk

        # 1. 找到 "data: " 的位置
        data_start = full_response.find("data: ") + len("data: ")
        # 2. 提取 data 部分
        data_str = full_response[data_start:].strip()

        # 将 data 字符串解析为 JSON 对象
        data = json.loads(data_str)

        # 获取 content 字段
        content = data["content"]

        # 保存 AI 回复到历史记录
        # 假设 add_message_to_chat 是你的函数
        add_message_to_chat(request.chat_id, "assistant", content)
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")
    