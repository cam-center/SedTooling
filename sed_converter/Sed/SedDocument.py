from pydantic import BaseModel
from typing import List, Union, Optional

from sed_converter.metadata.Metadata import Metadata
from sed_converter.dependencies.Dependency import Dependency
from sed_converter.declarations.Declarations import Declarations
from sed_converter.IO.Input import Input
from sed_converter.IO.Output import Output
from sed_converter.actions.Action import Action


class SedDocument(BaseModel):
    """
    This class serves as a stepping stone to access the metadata and parse for the correct version
    """
    Metadata: Metadata
    Dependencies: List[Dependency]
    Declarations: Declarations
    Inputs: Optional[List[Input]]
    Outputs: Optional[List[Output]]
    Actions: List[Action]


class SedDocumentL1V1(SedDocument, BaseModel):
    Metadata: Metadata
    Dependencies: List[Dependency]
    Declarations: Declarations
    Inputs: Optional[List[Input]]
    Outputs: Optional[List[Output]]
    Actions: List[Action]


def get_correct_doc(json_dict: dict) -> Union[SedDocumentL1V1]:
    level_version_matrix = [[SedDocumentL1V1]]
    document: Union[SedDocumentL1V1, SedDocument] = SedDocument(**json_dict)
    level: int = document.Metadata.level
    version: int = document.Metadata.version
    correct_release = level_version_matrix[level - 1][version - 1]
    try:
        temp_doc = correct_release(**json_dict)
        document = temp_doc
    except Exception as e:
        print(f"Document could not be processed as level:{level} version:{version}")
        raise e
    return document





