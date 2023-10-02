import re

from typing import List, Dict, Union, Optional

from pydantic import field_validator

from simulation import Simulation


class Cosimulation(Simulation):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        subpattern: str = "[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?"
        pattern: str = f"cosim::{subpattern}"
        assert re.fullmatch(pattern, v) is not None
        return v
