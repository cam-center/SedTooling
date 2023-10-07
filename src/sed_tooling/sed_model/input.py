import regex
from typing import List

from pydantic import BaseModel, field_validator


class Input(BaseModel):
    name: str
    identifier: str
    type: str
    target: str

    @classmethod
    @field_validator("identifier")
    def legal_id(cls, v: str) -> str:
        assert regex.fullmatch("[A-Za-z0-9_-]+", v) is not None
        return v

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert (
            regex.fullmatch("[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?", v)
            is not None
        )
        return v

    @classmethod
    @field_validator("target")
    def validate_interval_with_reference(cls, v: str) -> str:
        if isinstance(v, float) or isinstance(v, int):
            return str(float(v))
        if v.startswith("#"):
            assert regex.fullmatch("#[A-Za-z0-9_-]+", v) is not None
            return v
        else:
            # trip any exception converting to float
            float(v)
            return v  # but we don't want to return a float
