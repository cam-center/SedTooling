import regex
from typing import List, Union, Dict

from pydantic import BaseModel, field_validator

from action import Action
from pattens import Patterns


class DataReport(Action):
    type: str
    sim: List[str]
    metaData: Dict[str, Union[str, List[Union[str, float, int, bool]]]]
    dataSets: List[str]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"sed::DataReport", v) is not None
        return v


class HDF5Report(Action):
    type: str
    dataHierarchy: Dict[str, List[str]]

    @classmethod
    @field_validator("type")
    def type_must_be_properly_formed(cls, v: str) -> str:
        assert regex.fullmatch(Patterns.TYPE_PATTERN, v) is not None
        assert regex.fullmatch(f"hdf5::Hdf5Report", v) is not None
        return v

    @classmethod
    @field_validator("dataHierarchy")
    def check_data_hierarchy_values(
        cls, v: Dict[str, List[Union[Dict, str]]]
    ) -> Dict[str, List[Union[Dict, str]]]:
        for data_sets in v.values():
            assert len(data_sets) != 0
            for data_set in data_sets:
                if isinstance(data_set, str):
                    assert regex.fullmatch(Patterns.IDENTIFIER_REFERENCE, data_set) is not None
                else:
                    assert DataReport(**data_set)
        return v
