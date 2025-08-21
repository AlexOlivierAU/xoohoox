from pydantic import BaseModel
from datetime import date

class Batch(BaseModel):
    batch_id: str
    grower_id: int
    produce_type: str
    varietal: str
    dispatch_date: date
    quantity_kg: float