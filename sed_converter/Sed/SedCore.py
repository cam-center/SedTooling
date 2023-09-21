from typing import List

from SedDocument import SedDocument

import json



class SedCore:

    def __init__(self, sed_files: List[str]) -> None:
        self.files: List[str] = sed_files

    def validateFiles(self):
        decoded_files: List[dict] = [json.load(file) for file in self.files]
        print("validating Sed")

    def convertToSedML(self):
        print("converting Sed")

    def _combine_sed_documents(self, sed_documents: List[SedDocument]):
        pass