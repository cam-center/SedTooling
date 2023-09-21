from pydantic import BaseModel, field_validator
from typing import List

import re


class Input(BaseModel):
    name: str
    id: str
    type: str
    source: str
 
    @field_validator("id")
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
            assert re.match("[A-Za-z0-9_-]+", element) != None
        return v
    
    @field_validator("source")
    @classmethod
    def validate_interval_with_reference(cls, v: str) -> str:
        if isinstance(v, float):
            return str(v)
        if v.startswith("#"):
            assert re.match("#[A-Za-z0-9_-]+", v) != None
        else:
            # trip any exception converting to float
            int(v)
            return v  # but we don't want to return an int