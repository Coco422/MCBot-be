from pydantic import BaseModel

class LawSlice(BaseModel):
    law_name: str
    chapter: str
    article_content: str
    similarity: float