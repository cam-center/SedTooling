import regex
from typing import List, Union, Dict

from pydantic import BaseModel, field_validator

from action import Action
from pattens import Patterns


class Curve(Action):
    type: str
    sims: List[str]
    x_axis: str
    y_axis: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"plot::curve", v) is not None
        return v

    @classmethod
    @field_validator("sims")
    def check_sims(cls, v: str) -> str:
        for sim in v:
            assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, sim) is not None
        return v

    @classmethod
    @field_validator("x_axis", "y_axis")
    def check_axes(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, v) is not None
        return v


class Surface(Action):
    type: str
    sims: List[str]
    x_axis: str
    y_axis: str
    z_axis: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"plot::surface", v) is not None
        return v

    @classmethod
    @field_validator("sims")
    def check_sims(cls, v: str) -> str:
        for sim in v:
            assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, sim) is not None
        return v

    @classmethod
    @field_validator("x_axis", "y_axis", "z_axis")
    def check_axes(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, v) is not None
        return v


class Plot2D:
    type: str
    curves: List[Union[str, Dict]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"plot::2DPlot", v) is not None
        return v

    @classmethod
    @field_validator("curves")
    def check_curves(cls, v: List[Union[str, Dict]]):
        assert len(v) > 0
        for curve in v:
            if isinstance(curve, str):
                assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, curve) is not None
            elif isinstance(curve, dict):
                assert Curve(**curve)


class Plot3D:
    type: str
    surfaces: List[Union[str, Dict]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"plot::3DPlot", v) is not None
        return v

    @classmethod
    @field_validator("surfaces")
    def check_curves(cls, v: List[Union[str, Dict]]):
        assert len(v) > 0
        for surface in v:
            if isinstance(surface, str):
                assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, surface) is not None
            elif isinstance(surface, dict):
                assert Surface(**surface)
