import re
from typing import List, Union

from pydantic import BaseModel, field_validator


class Output(BaseModel):
    name: str
    identifier: str
    type: str
    interval: Union[float, str]

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

    @field_validator("interval")
    @classmethod
    def validate_interval_with_reference(cls, v: Union[float, str]) -> str:
        if isinstance(v, float):
            return str(v)
        if v.startswith("#"):
            assert re.match("#[A-Za-z0-9_-]+", v) is not None
        else:
            # trip any exception converting to float
            float(v)
            return v  # but we don't want to return an int
