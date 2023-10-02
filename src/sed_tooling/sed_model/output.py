import re
from typing import List, Union

from pydantic import BaseModel, field_validator


class Output(BaseModel):
    name: str
    identifier: str
    type: str
    interval: Union[float, str]

    @classmethod
    @field_validator("identifier")
    def legal_id(cls, v: str) -> str:
        assert re.match("[A-Za-z0-9_-]+", v) is not None
        return v

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert (
            re.match("[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?", v) is not None
        )
        return v

    @classmethod
    @field_validator("interval")
    def validate_interval_with_reference(cls, v: Union[float, str]) -> str:
        if isinstance(v, float):
            return str(v)
        if v.startswith("#"):
            assert re.match("#[A-Za-z0-9_-]+", v) is not None
            return v
        else:
            # trip any exception converting to float
            float(v)
            return v  # but we don't want to return an int
