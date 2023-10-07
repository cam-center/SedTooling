import regex

from pydantic import field_validator

from sed_tooling.sed_model.spatial_sim import SpatialSimulationSim, SpatialSimulationCosim
from sed_tooling.sed_model.nonspatial_sim import NonspatialSimulationSim, NonspatialSimulationCosim


class OneStepSimSpatial(SpatialSimulationSim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch("^sim::SpatialSimulation<OneStep>$", v) is not None
        return v


class OneStepCosimSpatial(SpatialSimulationCosim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch("^cosim::SpatialSimulation<OneStep>$", v) is not None
        return v


class OneStepSim(NonspatialSimulationSim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch("^sim::NonspatialSimulation<OneStep>$", v) is not None
        return v


class OneStepCosim(NonspatialSimulationCosim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch("^cosim::NonspatialSimulation<OneStep>$", v) is not None
        return v
