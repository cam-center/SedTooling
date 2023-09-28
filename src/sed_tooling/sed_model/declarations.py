from typing import List

from pydantic import BaseModel

from sed_tooling.sed_model.constant import Constant
from sed_tooling.sed_model.variable import Variable


class Declarations(BaseModel):
    constants: List[Constant]
    variables: List[Variable]
