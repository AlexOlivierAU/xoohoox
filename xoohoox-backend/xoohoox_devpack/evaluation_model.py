from pydantic import BaseModel

class Evaluation(BaseModel):
    sample_id: str
    score_aroma: int
    score_color: int
    score_taste: int
    evaluator_name: str
    comments: str