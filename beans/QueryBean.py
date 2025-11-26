from pydantic import BaseModel


class QueryBean(BaseModel):
    uiFieldName: str
    policyType: str
