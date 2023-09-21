from pydantic import BaseModel
from typing import List

from sed_converter.metadata.Metadata import Metadata
from sed_converter.dependencies.Dependency import Dependency
from sed_converter.declarations.Declarations import Declarations
from sed_converter.IO.Input import Input
from sed_converter.IO.Output import Output


class SedDocument:
    pass


class SedDocument_L1(SedDocument):
    pass


class SedDocument_L1_V1(BaseModel, SedDocument_L1):
    Metadata: Metadata
    Dependencies: List[Dependency]
    Declarations: Declarations
    Inputs: List[Input]
    Outputs: List[Output]
    Actions: List[Action]
    