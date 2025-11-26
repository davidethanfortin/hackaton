from pydantic import BaseModel
from typing import List

class RequestBean(BaseModel):
    table_name: str
    json_column: str
    json_path: str
    natural_language_query: str
    policy_types: List[str]
