from pydantic import BaseModel
from typing import List

class YeastStrain(BaseModel):
    strain_name: str
    genetic_notes: str
    function_tags: List[str]
    origin: str
    last_tested_batch: str