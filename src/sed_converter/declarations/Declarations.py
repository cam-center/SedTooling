from pydantic import BaseModel
from typing import List

from sed_converter.declarations.constants.Constant import Constant
from sed_converter.declarations.variables.Variable import Variable


class Declarations(BaseModel):
    Constants: List[Constant]
    Variables: List[Variable]
