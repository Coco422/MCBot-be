from pydantic import BaseModel

class Question(BaseModel):
    id: int
    q_stem: str
    q_type: str
    options: str
    answer: str