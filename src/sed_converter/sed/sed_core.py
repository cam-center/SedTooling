import json

from pathlib import Path
from typing import List, Dict

from sed_converter.sed.sed_document import SedDocument, get_correct_doc


class SedCore:
    def __init__(self, sed_files: List[str]) -> None:
        self.files: List[str] = sed_files
        self.parsed_files: Dict[str, SedDocument] = {}

    def validate_all_files(self) -> None:
        for file in self.files:
            print(f"parsing {file}:\n\n\n")
            with Path(file).open("r") as sed:
                contents = sed.read()
                self.parsed_files[file] = get_correct_doc(json.loads(contents))

    def convert_to_sedml(self, sed_doc: SedDocument) -> None:
        ontologies: list[str] = sed_doc.metadata.ontologies
        # unsupported ontologies
        if {"pe", "cosim"}.intersection(set(ontologies)):
            raise NotImplementedError(
                "File contains ontologies that can not currently be converted to SedML"
            )
        print("converting Sed")

    def convert_all_sedml(self) -> None:
        print("converting Sed")

    def _combine_sed_documents(self, sed_documents: List[SedDocument]) -> None:
        pass  # Not yet implemented
