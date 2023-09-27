from pydantic import BaseModel, field_validator
from typing import List
import re


class Dependency(BaseModel):
    name: str
    identifier: str
    type: str
    source: str

    @field_validator("identifier")
    @classmethod
    def legal_id(cls, v: str) -> str:
        assert re.match("[A-Za-z0-9_-]+", v) != None
        return v

    @field_validator("type")
    @classmethod
    def type_must_be_properly_formed(cls, v: str) -> str:
        parts: List[str] = re.split("::", v)
        assert len(parts) >= 2
        for element in parts:
            assert re.match("[><A-Za-z0-9_-]+", element) != None
        return v

    @field_validator("source")
    @classmethod
    def legal_source(cls, v: str) -> str:
        assert re.match("[A-Za-z0-9_\\/-]+", v) != None
        return v
