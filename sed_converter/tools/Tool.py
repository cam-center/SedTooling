from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    identifier: str