import re

from typing import List, Dict, Union, Optional

from pydantic import field_validator

from action import Action


class Simulation(Action):
    type: str
    model: str
    algorithm: str
    algorithmParameters: Optional[Dict[str, Union[bool, str, float, int]]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        subpattern: str = "[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?"
        pattern: str = f"sim::{subpattern}"
        assert re.fullmatch(pattern, v) is not None
        return v

    @classmethod
    @field_validator("model")
    def legal_model(cls, v: str) -> str:
        assert re.match("#[A-Za-z0-9_-]+", v) is not None
        return v

    @classmethod
    @field_validator("algorithm")
    def legal_algorithm(cls, v: str) -> str:
        parts: List[str] = re.split(":", v)
        assert len(parts) >= 2
        for element in parts:
            if len(element) == 0:
                continue
            assert re.match("[><A-Za-z0-9_-]+", element) is not None
        return v

    @classmethod
    @field_validator("algorithmParameters")
    def legal_parameters(cls, v: Optional[Dict[str, Union[bool, str, float, int]]]):
        if v is None:
            return v
        keys: list[str] = [val.strip() for val in v.keys()]
        assert len(keys) == len(set(keys))

        values: list[Union[bool, str, float, int]] = list(v.values())
        for value in values:
            assert (
                isinstance(value, bool)
                or isinstance(value, str)
                or isinstance(value, float)
                or isinstance(value, int)
            )
        return str(v)


class LoopedSimulation(Action):
    type: str
    sim: str
    modelReset: Union[str, bool]
    parameterScan: Union[str, bool]
    overrides: Dict[str, str]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert (
            re.fullmatch("[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?", v)
            is not None
        )
        return v

    @classmethod
    @field_validator("sim")
    def legal_model(cls, v: str) -> str:
        assert re.match("#[A-Za-z0-9_-]+", v) is not None
        return v

    @classmethod
    @field_validator("modelReset", "parameterScan")
    def legal_boolean_check(cls, v: Union[str, bool]) -> str:
        if isinstance(v, str):
            v = bool(v)  # we want to throw an exception if it's not actually a boolean
        return str(v)  # but we want a string

    @classmethod
    @field_validator("overrides")
    def legal_overrides(cls, v: Dict[str, str]):
        keys = list(v.keys())
        assert len(keys) == len(set(keys))
        for value in list(v.values()):
            if re.fullmatch("sed::range\(.+\)", value) is not None:
                substr: str = value[11:-1]
                parts: list[float] = [float(part.strip()) for part in substr.split(",")]
                assert 0 < len(parts) < 4
            elif (
                re.fullmatch("\[( *#?[A-Za-z0-9._-]+ *, *)*(#?[A-Za-z0-9._-]+)\]", value)
                is not None
            ):
                parts: list[str] = [part.strip() for part in value[1:-1].split(",")]
                for part in parts:
                    assert (
                        re.fullmatch("([0-9]+[.])?[0-9]+", part) is not None
                        or re.fullmatch("#[A-Za-z0-9_-]+", part) is not None
                    )
            else:
                raise ValueError(f"Unknown value: `{value}` in value of Simulation's overrides.")
