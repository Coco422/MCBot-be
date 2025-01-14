from models.question import Question
from models.law import LawSlice
from models.analysis import AnalysisResponse
from fastapi import HTTPException
import random
from database.connection import get_db_connection, release_db_connection

# 可用题目 ID
QUESTION_IDS = [12975, 12995, 13007, 12956, 12958, 12962, 12934, 12977, 13019, 12946, 12902, 13022, 12938, 12988, 12985, 12935, 12896, 13040, 12901, 12971, 12997, 12961, 12982, 12895, 13037, 12891, 12973, 12916, 13009, 12984, 13015, 12980, 12954, 13000, 12930, 12892, 12903, 12952, 13027, 13063, 12948, 12909, 13054, 12993, 13048, 12926, 12967, 12942, 12918, 12912, 12897, 12950, 13011, 12965, 12969, 12941, 13003, 13016, 13046, 13117, 12999, 12944, 13032, 12990, 12908, 12914, 13018, 13077, 12960, 12906, 13005, 12983, 12932, 12924, 12890, 12921, 12928, 12915, 12898, 13013]

def get_law_slices_by_question_id(question_id: int) -> list[LawSlice]:
    """
    根据题目ID获取对应的法条切片
    """
    print(question_id)
    connection = None
    try:
        # 获取数据库连接
        connection = get_db_connection()
        cursor = connection.cursor()

        # 执行 SQL 查询
        query = """
            SELECT law_name, chapter, article_content, similarity 
            FROM tobacco.get_top_laws_by_similarity(%s)
        """
        cursor.execute(query, (question_id,))
        results = cursor.fetchall()

        # 将查询结果转换为 LawSlice 对象列表
        law_slices = []
        for row in results:
            law_slice = LawSlice(
                law_name=row[0], 
                chapter=row[1], 
                article_content=row[2], 
                similarity=row[3]
            )
            law_slices.append(law_slice)

        return law_slices
    except Exception as e:
        raise Exception(f"获取法条切片失败: {str(e)}")
    finally:
        # 释放数据库连接
        if connection:
            release_db_connection(connection)


def get_random_question() -> Question:
    """
    随机获取一道题目
    """
    connection = None
    try:
        # 随机选择一个题号
        question_id = random.choice(QUESTION_IDS)

        # 获取数据库连接
        connection = get_db_connection()
        cursor = connection.cursor()

        # 执行 SQL 查询
        query = """
            SELECT q_stem, q_type, options, answer 
            FROM tobacco.te_exam_question 
            WHERE que_id = %s
        """
        cursor.execute(query, (question_id,))
        result = cursor.fetchone()

        if not result:
            raise Exception("未找到对应的题目")
        print(result)
        # 返回题目数据
        return Question(
            id=question_id,
            q_stem=result[0],  
            q_type=result[1],
            options=result[2],  
            answer=result[3], 
        )
    except Exception as e:
        raise Exception(f"获取题目失败: {str(e)}")
    finally:
        # 释放数据库连接
        if connection:
            release_db_connection(connection)
            
def get_analysis_by_question_id(question_id: int) -> AnalysisResponse:
    """
    根据题目 ID 获取 AI 生成的法律分析内容
    """
    connection = None
    try:
        # 获取数据库连接
        connection = get_db_connection()
        cursor = connection.cursor()

        # 执行 SQL 查询
        query = """
            SELECT analysis_qwen32 
            FROM tobacco.exam_questions 
            WHERE id = %s
        """
        cursor.execute(query, (question_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=4004, detail="未找到对应的法律分析内容")

        # 返回法律分析内容
        return AnalysisResponse(
            analysis=result[0],  # analysis_qwen32
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=5000, detail=f"获取法律分析内容失败: {str(e)}")
    finally:
        # 释放数据库连接
        if connection:
            release_db_connection(connection)

