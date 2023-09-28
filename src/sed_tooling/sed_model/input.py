import re
from typing import List

from pydantic import BaseModel, field_validator


class Input(BaseModel):
    name: str
    identifier: str
    type: str
    target: str

    @field_validator("identifier")
    @classmethod
    def legal_id(cls, v: str) -> str:
        assert re.match("[A-Za-z0-9_-]+", v) is not None
        return v

    @field_validator("type")
    @classmethod
    def type_must_be_properly_formed(cls, v: str) -> str:
        parts: List[str] = re.split("::", v)
        assert len(parts) >= 2
        for element in parts:
            assert re.match("[><A-Za-z0-9_-]+", element) is not None
        return v

    @field_validator("target")
    @classmethod
    def validate_interval_with_reference(cls, v: str) -> str:
        if isinstance(v, float) or isinstance(v, int):
            return str(float(v))
        if v.startswith("#"):
            assert re.match("#[A-Za-z0-9_-]+", v) is not None
            return v
        else:
            # trip any exception converting to float
            int(v)
            return v  # but we don't want to return an int
