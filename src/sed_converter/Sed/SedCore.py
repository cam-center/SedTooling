from typing import List, Dict

from sed_converter.Sed.SedDocument import SedDocument, get_correct_doc

import json


class SedCore:
    def __init__(self, sed_files: List[str]) -> None:
        self.files: List[str] = sed_files
        self.parsed_files: Dict[str, SedDocument] = {}

    def validateAllFiles(self):
        for file in self.files:
            print(f"parsing {file}:\n\n\n")
            with open(file, "r") as sed:
                contents = sed.read()
                self.parsed_files[file] = get_correct_doc(json.loads(contents))

    def convertToSedML(self, sed_doc: SedDocument):
        ontologies: list[str] = sed_doc.Metadata.Ontologies
        # unsupported ontologies
        if {"pe", "cosim"}.intersection(set(ontologies)):
            raise NotImplementedError(
                "File contains ontologies that can not currently be converted to SedML"
            )
        print("converting Sed")

    def convertAllSedML(self):
        print("converting Sed")

    def _combine_sed_documents(self, sed_documents: List[SedDocument]):
        pass  # Not yet implemented
