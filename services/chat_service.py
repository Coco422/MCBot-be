import asyncio
import time
from fastapi import HTTPException

from tools.utils import deprecated
from tools.openai_chat import get_chat_response_stream_httpx, get_chat_response_stream_langchain, get_chat_response
from services.tobacco_study import get_random_question
from tools.embedding_service import embedding_service
from models.question import Question
from models.law import LawSlice
from database.connection import get_db_connection, release_db_connection

from typing import AsyncIterator, List
from models.chat import ChatTrainRequest, ChatAnalysisRequest
import uuid
import json
from psycopg2.extras import Json

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
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
    if chat_id in chat_history_map:
        return chat_history_map[chat_id]
    else:
        messages = load_chat_from_db(chat_id)
        if messages:
            chat_history_map[chat_id] = messages
        return messages

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

def add_message_to_chat(chat_id, role, content):
    """向对话历史中添加消息"""
    if chat_id not in chat_history_map:
        chat_history_map[chat_id] = []
    chat_history_map[chat_id].append({"role": role, "content": content})
    # 同步到数据库
    save_chat_to_db(chat_id, chat_history_map[chat_id])

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

async def chat_with_ai(request: ChatTrainRequest) -> AsyncIterator[str]:
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
            try:
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
                yield f"event:rag\n{rag_context}\n\n"
                user_input_with_kb = f"""\
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
            except:
                # 如果问题id出错
                # 调用RAG搜索
                rag_question_low_results = await rag_search(request.user_input)
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
                yield f"event:rag\n{rag_context}\n\n"
                user_input_with_kb = f"""
相关文档:
{rag_context}

用户当前查看题目信息:
无

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
    except json.JSONDecodeError as e:
        logger.error("json 解析失败")
        pass
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"AI 模块错误，请联系管理员: {str(e)}")

async def optimize_query_with_llm(query: str) -> str:
    """
    使用LLM优化用户查询
    """
    messages = [{"role": "user", "content": f"""
                 请优化以下用户的询问语句，使其更清晰准确:\n{query}
如果用户的语句足够清晰，直接输出用户的语句即可
如果用户表达的意思混乱，不要进行询问。尽可能的优化成正常的问句。不要对内容进行修改。
直接输出优化结果，不要进行询问
"""}]
    return await get_chat_response(messages)

async def select_table(query: str) -> dict:
    """
    根据查询选择适当的表格
    """
    # 这里可以根据数据库schema信息选择表格
    # 示例实现，实际应根据具体数据库schema调整
    return """
[DB_ID] tobacco
[Schema]
# Table: exam_question
[
  (id:INTEGER, Primary Key, the unique identifier of the exam question, Auto-increment, Examples:[1, 2, 3814]),
  (question:TEXT, the question text, Examples:["25据《烟草专卖法》的规定，烟草专卖行政主管部门主要负责查处下列案件（      ）。"]),
  (solution:TEXT, the solution text, Examples:["C|D"]),
  (options:TEXT, the options text, Examples:["A.假冒商标卷烟|B.无烟草专卖零售许可证经营烟草专卖品|C.违法收购烟叶|D.无证运输烟草专卖品"]),
  (slice_no:INTEGER, the related slice chapter number, Optional, Examples:[1, 2, 5]),
  (law_content:TEXT, the law content related to the question, Examples:["第三十三条 生产、销售没有注册商标的卷烟、雪茄烟、有包装的烟丝的，由工商行政管理部门责令停止生产、销售，并处罚款。  

生产、销售假冒他人注册商标的烟草制品的，由工商  

行政管理部门责令停止侵权行为，赔偿被侵权人的损失，可以并处罚款；构成犯罪的，依法追究刑事责任。
第二十条的规定，非法印制烟草制品商标标识的，由工商行政管理部门销毁印制的商标标识，没收违法所得，并处罚款。
第三十条 有关部门依法查获的假冒商标烟草制品，应当交由烟草专卖行政主管部门按照国家有关规定公开销毁，禁止以任  

何方式销售。
第一条 生产、销售伪劣卷烟、雪茄烟等烟草专卖品，销售金额在五万元以上的，依照刑法第一百四十条的规定，以生产、销售伪劣产品罪定罪处罚。未经卷烟、雪茄烟等烟草专卖品注册商标所有人许可，在卷烟、雪茄烟等烟草专卖品上使用与其注册商标相同的商标，情节严重的，依照刑法第二百一十三条的规定，以假冒注册商标罪定罪处罚。销售明知是假冒他人注册商标的卷烟、雪茄烟等烟草专卖品，销售金额较大的，依照刑法第二百一十四条的规定，以销售假冒注册商标的商品罪定罪处罚。伪造、擅自制造他人卷烟、雪茄烟注册商标标识或者销售伪造、擅自制造的卷烟、雪茄烟注册商标标识，情节严重的，依照刑法第二百一十五条的规定，以非法制造、销售非法制造的注册商标标识罪定罪处罚。违反国家烟草专卖管理法律法规，未经烟草专卖行政主管部门许可，无烟草专卖生产企业许可证、烟草专卖批发企业许可证、特种烟草专卖经营企业许可证、烟草专卖零售许可证等许可证明，非法经营烟草专卖品，情节严重的，依照刑法第二百二十五条的规定，以非法经营罪定罪处罚。
第十九条 卷烟、雪茄烟和有包装的烟丝必须申请商标注册，未经核准注册的，不得生产、销售。  

禁止生产、销售假冒他人注册商标的烟草制品。"])
]

[DB_ID] tobacco
[Schema]
# Table: exam_user_answer
[
  (questionid:INTEGER, NOT NULL, the question identifier, Maps to exam_question.id, Examples:[1, 2, 3]),
  (score:NUMERIC(9,2), NOT NULL, the score of the answer, Examples:[2, 3.33]),
   (examuserrecordid:VARCHAR(100), the GUID value of the exam record,  Examples:["cc4fc0e4344547dcab5b6e19083c1bdc"])
]
"""

def generate_sql_reasoning(query: str, table_info: dict) -> AsyncIterator[str]:
    """
    生成SQL查询的推理过程
    """
    messages = [{
        "role": "user",
        "content": f"""
        请解释如何根据以下查询生成SQL:
        查询: {query}
        表格信息: {table_info}
        请详细说明查询逻辑和步骤,不要生成 sql 语句
        """
    }]
    return get_chat_response_stream_langchain(messages)

def final_output(query:str, query_result:str)-> AsyncIterator[str]:
    """
    生成结果的回答
    """
    messages = [{
        "role": "user",
        "content": f"""
        接下来提供给你用户的查询语句和查到的结果（结果以markdown形式给到你）
        查询: {query}
        查询结果: {query_result}
        根据查询结果，回答用户的问题，不要有多余的废话和解释。仅友好的回答问题即可
        如果查询结果无法推断回答用户问题，则告知。“非常抱歉，无法从已查询内容回答您的问题”
        """
    }]
    return get_chat_response_stream_langchain(messages)

async def generate_sql(query: str, table_info: dict, reasoning: str) -> str:
    """
    根据推理生成SQL查询
    
    Args:
        query: 自然语言查询
        table_info: 表格信息
        reasoning: 推理过程
        
    Returns:
        生成的SQL查询语句
    """

    prompt = """You are now a PostgreSQL data analyst, and you are given a database schema as follows:

【Schema】
{db_schema}

【Question】
{question}

【Evidence】
{evidence}

Please read and understand the database schema carefully, and generate an executable SQL based on the user's question and evidence. 
The generated SQL is protected by json like this{{"sql":""}}.
**IMPORTANT**
remember only output the sql by json.Do not explain
""".format(question=query, db_schema=table_info, evidence=reasoning)
    
    messages = [{
        "role": "user",
        "content": prompt
    }]
    llm_response = await get_chat_response(messages, if_json=True)
    # 提取 SQL 语句
    if isinstance(llm_response, dict):
        return llm_response.get("sql") or llm_response.get("SQL") or llm_response
    return llm_response

async def format_results(results: List[tuple], sql_query: str, user_query: str) -> str:
    """
    格式化SQL查询结果
    """
    if not results:
        return "查询结果集无内容"
    
    # 构造messages，要求LLM根据SQL语句和查询结果输出前端绘图用数据
    messages = [{
        "role": "user",
        "content": f"""
接下来给到你的是一个 SQL 查询语句 、一个 SQL 查询结果、以及用户查询的问题
你需要根据结果输出标准的 json 样式，用来画柱状图
样式样例如下
帮我查询第一周的考试数量
{{"categories": ["Mon1", "Tue1", "Wed1", "Thu1", "Fri1", "Sat1", "Sun1"],
"values": [120, 200, 150, 80, 70, 110, 130]}}
你需要输出这样子的格式{{"categories":[],"values":[]}}
---
SQL查询：
{sql_query}
---
查询结果：
{results}
---
用户查询问题
{user_query}
---
接下来输出标准的 json 结构
请确保你必须输出这样的格式，包含categories和values两个键，里面是数组{{"categories":[],"values":[]}}
        """
    }]
    
    logger.debug(messages)
    llm_response = await get_chat_response(messages,if_json=True)
    
    return llm_response

async def chat_with_ai_analysis(request: ChatAnalysisRequest) -> AsyncIterator[str]:
    """
    与 AI 进行数据分析对话，生成 SQL 并执行查询
    :param request: 包含用户输入和数据库ID的请求
    :return: 返回查询结果的流式响应
    """
    conn = None 
    # 预留设计
    database_id = request.database_id
    user_query = request.user_input
    chat_id = request.chat_id
    
    try:
        # step 1: 优化用户问题
        yield "event:step1\ndata:优化用户的问题\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("1. 开始优化用户的问题")
        optimized_query = await optimize_query_with_llm(user_query)
        yield f"event:update\ndata:{optimized_query}\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        # step 2: 选择表格
        yield "event:step2\ndata:选择表格中\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("2. 选择表格，返回表格信息")
        table_info = await select_table(optimized_query)
        yield f"event:update\ndata:Form has been selected, form information has been prepared\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        # step 3: 生成SQL推理过程
        yield "event:step3\ndata:生成 SQL 推理过程\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("3. 生成 SQL 推理过程解释")
        reasoning = generate_sql_reasoning(optimized_query, table_info)
        async for chunk in reasoning:
            yield chunk
        # yield f"event:update\ndata:evidence for generate: {reasoning}\n\n"
        
        # step 4: 生成SQL
        yield "event:step4\ndata:生成 sql 并提取\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("4. 生成 sql 并提取")
        sql_query = await generate_sql(optimized_query, table_info, reasoning)
        yield f"event:update\ndata:{sql_query}\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒

        # step 5: 执行SQL
        yield "event:step5\ndata: 执行 sql\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("5. 执行 sql")
        db_type = "prod"
        conn = get_db_connection(db_type)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        logger.debug(results)
        yield f"event:update\ndata:SQL执行成功，获取到{len(results)}条结果\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒

        # step 6: 格式化结果
        yield "event:step6\ndata:格式化结果\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("6.格式化结果")
        formatted_results = await format_results(results, sql_query, optimized_query)
        yield f"event:sqldata\ndata:{formatted_results}\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        yield f"event:update\ndata:格式化成功\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒

        # step 7: 保存结果
        yield "event:step7\ndata:保存结果\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("7. 保存结果")
        add_message_to_chat(chat_id, "assistant", f"SQL查询结果:\n{formatted_results}")
        yield "event:update\ndata:结果已保存到对话历史\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        # step 8: 最终输出
        yield "event:step8\ndata:最终输出\n\n"
        await asyncio.sleep(0.01)  # 异步睡眠 10 毫秒
        logger.warning("8. 最终输出")
        final_output_from_llm = final_output(optimized_query, formatted_results)
        async for chunk_output in final_output_from_llm:
            yield chunk_output
        
    except Exception as e:
        logger.error(f"SQL执行失败: {e}")
        yield f"event:ERROR\ndata:SQL执行失败: {str(e)}\n\n"
    finally:
        if conn:
            release_db_connection(conn,db_type=db_type)
    
