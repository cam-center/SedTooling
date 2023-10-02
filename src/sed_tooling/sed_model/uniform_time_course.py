import re

from typing import Optional, Union

from pydantic import field_validator

from sed_tooling.sed_model.nonspatial_sim import NonspatialSimulationSim, NonspatialSimulationCosim
from sed_tooling.sed_model.spatial_sim import SpatialSimulationSim, SpatialSimulationCosim


class UniformTimeCourseSim(NonspatialSimulationSim):
    type: str
    numDataPoints: Union[str, int]
    endTime: Union[str, float]
    startTime: Optional[Union[str, float]]
    outputStartTime: Optional[Union[str, float]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^sim::NonspatialSimulation<UTC>$", v) is not None
        return v

    @classmethod
    @field_validator("numDataPoints")
    def validate_points(cls, v: Union[str, int]) -> str:
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = int(v)  # we want to throw an exception if it's not actually an integer
        return str(v)  # but we want a string

    @classmethod
    @field_validator("endTime", "startTime", "outputStartTime")
    def validate_times(cls, v: Optional[Union[str, float]]) -> Optional[str]:
        if v is None:
            return v
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = float(v)  # we want to throw an exception if it's not actually a boolean
        return str(v)  # but we want a string


class UniformTimeCourseSimSpatial(SpatialSimulationSim):
    type: str
    numDataPoints: Union[str, int]
    endTime: Union[str, float]
    startTime: Optional[Union[str, float]]
    outputStartTime: Optional[Union[str, float]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^sim::SpatialSimulation<UTC>$", v) is not None
        return v

    @classmethod
    @field_validator("numDataPoints")
    def validate_points(cls, v: Union[str, int]) -> str:
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = int(v)  # we want to throw an exception if it's not actually an integer
        return str(v)  # but we want a string

    @classmethod
    @field_validator("endTime", "startTime", "outputStartTime")
    def validate_times(cls, v: Optional[Union[str, float]]) -> Optional[str]:
        if v is None:
            return v
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = float(v)  # we want to throw an exception if it's not actually a boolean
        return str(v)  # but we want a string


class UniformTimeCourseCosim(NonspatialSimulationCosim):
    type: str
    numDataPoints: Union[str, int]
    endTime: Union[str, float]
    startTime: Optional[Union[str, float]]
    outputStartTime: Optional[Union[str, float]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^cosim::NonspatialSimulation<UTC>$", v) is not None
        return v

    @classmethod
    @field_validator("numDataPoints")
    def validate_points(cls, v: Union[str, int]) -> str:
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = int(v)  # we want to throw an exception if it's not actually an integer
        return str(v)  # but we want a string

    @classmethod
    @field_validator("endTime", "startTime", "outputStartTime")
    def validate_times(cls, v: Optional[Union[str, float]]) -> Optional[str]:
        if v is None:
            return v
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = float(v)  # we want to throw an exception if it's not actually a boolean
        return str(v)  # but we want a string


class UniformTimeCourseCosimSpatial(SpatialSimulationCosim):
    type: str
    numDataPoints: Union[str, int]
    endTime: Union[str, float]
    startTime: Optional[Union[str, float]]
    outputStartTime: Optional[Union[str, float]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^cosim::SpatialSimulation<UTC>$", v) is not None
        return v

    @classmethod
    @field_validator("numDataPoints")
    def validate_points(cls, v: Union[str, int]) -> str:
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = int(v)  # we want to throw an exception if it's not actually an integer
        return str(v)  # but we want a string

    @classmethod
    @field_validator("endTime", "startTime", "outputStartTime")
    def validate_times(cls, v: Optional[Union[str, float]]) -> Optional[str]:
        if v is None:
            return v
        if isinstance(v, str) and re.fullmatch("#[A-Za-z0-9_-]+", v) is None:
            v = float(v)  # we want to throw an exception if it's not actually a boolean
        return str(v)  # but we want a string
