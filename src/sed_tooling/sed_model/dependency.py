import regex
from typing import List

from pydantic import BaseModel, field_validator


class Dependency(BaseModel):
    name: str
    identifier: str
    type: str
    source: str

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
    @field_validator("source")
    def legal_source(cls, v: str) -> str:
        assert regex.fullmatch("[A-Za-z0-9_\\/-]+", v) is not None
        return v
