import regex
from typing import List

from pydantic import BaseModel, field_validator

from pattens import Patterns


class Action(BaseModel):
    name: str
    identifier: str
    type: str

    @classmethod
    @field_validator("identifier")
    def legal_id(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.IDENTIFIER_PATTERN, v) is not None
        return v

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        return v


class PerformMath(Action):
    type: str
    expression: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch("sed::performMath", v) is not None
        return v
