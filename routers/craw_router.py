from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database.connection import DatabasePool

# Define request and response models
class ArticleRequest(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    keyword: Optional[str] = None
    source: Optional[str] = None
    editor: Optional[str] = None

class ArticleResponse(BaseModel):
    total_count: int
    la_id: int
    user_name: str
    keyword: str
    title: str
    subtitle: str
    publish_time: str
    content: str
    source: str
    editor: str
    create_time: str

class KeywordRequest(BaseModel):
    keyword: str

class ChatRequest(BaseModel):
    keyword: str
    question: str

# Initialize the router
craw_router = APIRouter(prefix="/craw", tags=["craw"])

# Database connection
db_pool = DatabasePool()

@craw_router.post("/getArticleData", response_model=List[ArticleResponse])
async def get_article_data(request: ArticleRequest):
    # Implement the logic to fetch article data from the database
    query = "SELECT * FROM csm.query_articles(%s, %s, %s, %s, %s, 1, 5);"
    params = (request.category, request.title, request.keyword, request.source, request.editor)
    with db_pool.get_connection() as conn:
        with conn.cursor() as cur:
            await cur.execute(query, params)
            results = await cur.fetchall()
            # Process results into ArticleResponse
            return [ArticleResponse(**dict(result)) for result in results]

@craw_router.post("/getArticleDataByKeyword", response_model=List[ArticleResponse])
async def get_article_data_by_keyword(request: KeywordRequest):
    # Implement the logic to fetch articles by keyword
    query = "SELECT * FROM csm.te_lg_articles WHERE keyword = %s;"
    with db_pool.get_connection() as conn:
        with conn.cursor() as cur:
            await cur.execute(query, (request.keyword,))
            results = await cur.fetchall()
            return [ArticleResponse(**dict(result)) for result in results]
