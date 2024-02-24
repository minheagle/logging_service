from pydantic import BaseModel

class Log(BaseModel):
    method: str
    path: str