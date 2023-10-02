import re
from typing import List

from pydantic import BaseModel, field_validator


class Variable(BaseModel):
    name: str
    identifier: str
    type: str

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
