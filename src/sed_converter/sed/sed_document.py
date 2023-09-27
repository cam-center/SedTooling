from typing import List, Union, Optional

from pydantic import BaseModel

from sed_converter.actions.action import Action
from sed_converter.declarations.declarations import Declarations
from sed_converter.dependencies.dependency import Dependency
from sed_converter.io.input import Input
from sed_converter.io.output import Output
from sed_converter.metadata.metadata import Metadata


class SedDocument(BaseModel):
    """
    This class serves as a stepping stone to access the metadata and parse for the correct version
    """

    metadata: Metadata
    dependencies: List[Dependency]
    declarations: Declarations
    actions: List[Action]
    inputs: Optional[List[Input]] = None
    outputs: Optional[List[Output]] = None


class SedDocumentL1V1(SedDocument, BaseModel):
    metadata: Metadata
    dependencies: List[Dependency]
    declarations: Declarations
    actions: List[Action]
    inputs: Optional[List[Input]] = None
    outputs: Optional[List[Output]] = None


def get_correct_doc(json_dict: dict) -> SedDocumentL1V1:
    level_version_matrix = [[SedDocumentL1V1]]
    document: Union[SedDocumentL1V1, SedDocument] = SedDocument(**json_dict)
    level: int = document.metadata.level
    version: int = document.metadata.version
    correct_release = level_version_matrix[level - 1][version - 1]
    try:
        temp_doc = correct_release(**json_dict)
        document = temp_doc
    except Exception as e:
        print(f"Document could not be processed as level:{level} version:{version}")
        raise e
    return document
