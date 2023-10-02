import re
from typing import List

from pydantic import BaseModel, field_validator

from sed_tooling.sed_model.action import Action


class Load(Action):
    name: str
    identifier: str
    type: str
    source: str
    target: str

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
    @field_validator("source", "target")
    def validate_source_and_target(cls, v: str) -> str:
        assert re.match("#[><A-Za-z0-9_-]+", v) is not None
        return v
