from typing import List, Union

from pydantic import BaseModel, field_validator


class Metadata(BaseModel):
    name: str
    level: int
    version: int
    ontologies: List[str]

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

    @field_validator("ontologies")
    @classmethod
    def verify_ontologies(cls, v: List[str]) -> List[str]:
        valid_ontologies = [
            "sed",
            "pe",
            "output",
            "csv",
            "hdf5",
            "plot",
            "modeling",
            "sbml",
            "simulation",
            "sim",
            "cosim",
            "BioSim",
            "KiSAO",
        ]
        for ontology in v:
            assert ontology in valid_ontologies
        return v
