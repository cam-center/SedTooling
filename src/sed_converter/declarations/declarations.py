from typing import List

from pydantic import BaseModel

from sed_converter.declarations.constants.constant import Constant
from sed_converter.declarations.variables.variable import Variable


class Declarations(BaseModel):
    Constants: List[Constant]
    Variables: List[Variable]
