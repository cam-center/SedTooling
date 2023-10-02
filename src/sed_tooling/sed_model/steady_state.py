import re

from pydantic import field_validator

from sed_tooling.sed_model.spatial_sim import SpatialSimulationSim, SpatialSimulationCosim
from sed_tooling.sed_model.nonspatial_sim import NonspatialSimulationSim, NonspatialSimulationCosim


class SteadyStateSimSpatial(SpatialSimulationSim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^sim::SpatialSimulation<SteadyState>$", v) is not None
        return v


class SteadyStateCosimSpatial(SpatialSimulationCosim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^cosim::SpatialSimulation<SteadyState>$", v) is not None
        return v


class SteadyStateSim(NonspatialSimulationSim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^sim::NonspatialSimulation<SteadyState>$", v) is not None
        return v


class SteadyStateCosim(NonspatialSimulationCosim):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert re.fullmatch("^cosim::NonspatialSimulation<SteadyState>$", v) is not None
        return v
