import re
from typing import List

from pydantic import BaseModel, field_validator

from sed_converter.actions.action import Action


class Load(Action):
    name: str
    identifier: str
    type: str
    source: str
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

    @field_validator("source", "target")
    @classmethod
    def validate_source_and_target(cls, v: str) -> str:
        assert re.match("#[><A-Za-z0-9_-]+", v) is not None
        return v
