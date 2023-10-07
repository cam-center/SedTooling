import regex
from typing import Union

from pydantic import BaseModel, field_validator

from pattens import Patterns


class Variable(BaseModel):
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


class BasicVariable(Variable):
    source: str


class Model(Variable):
    type: str
    bindings: dict[str, str]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        #  f"modeling::Model(<( *{Patterns.TYPE_PATTERN} *, *)*{Patterns.TYPE_PATTERN}>)?"
        assert regex.fullmatch(f"modeling::Model(<{Patterns.TYPE_CHARS}>)?", v) is not None
        if v.endswith(">"):
            assert regex.fullmatch(f"{Patterns.TYPE_PATTERN}", v[16:-1])
        return v
