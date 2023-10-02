import re

from pydantic import field_validator

from sed_tooling.sed_model.simulation import Simulation
from sed_tooling.sed_model.cosimulation import Cosimulation


class SpatialSimulationSim(Simulation):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        subpattern: str = "[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?"
        pattern: str = f"sim::SpatialSimulation<{subpattern}>"
        assert re.fullmatch(pattern, v) is not None
        return v


class SpatialSimulationCosim(Cosimulation):
    type: str

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        subpattern: str = "[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?"
        pattern: str = f"cosim::SpatialSimulation<{subpattern}>"
        assert re.fullmatch(pattern, v) is not None
        return v
