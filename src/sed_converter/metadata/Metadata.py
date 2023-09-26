from pydantic import BaseModel, field_validator
from typing import Union, List

from sed_converter.ontologies.Ontology import Ontology


class Metadata(BaseModel):
    name: str
    level: int
    version: int
    Ontologies: List[str]


    @field_validator("level")
    @classmethod
    def check_level(cls, v: Union[str, int]) -> int:
        if isinstance(v, str):
            v = int(v)
        assert v > 0
        assert v < 2
        return v

    @field_validator("version")
    @classmethod
    def check_version(cls, v: Union[str, int]) -> int:
        if isinstance(v, str):
            v = int(v)
        assert v > 0
        assert v < 2
        return v

    @field_validator("Ontologies")
    @classmethod
    def verify_ontologies(cls, v: List[str]) -> List[str]:
        valid_ontologies = ["sed", "pe", "output", "csv", "hdf5", "plot", "modeling", 
                            "sbml", "simulation", "sim", "cosim", "BioSim", "KiSAO"]
        for ontology in v:
            assert ontology in valid_ontologies
        return v