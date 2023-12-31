import json
from pathlib import Path
from typing import Dict, List

from sed_tooling.sed_model.sed_document import SedDocument, get_correct_doc
from sed_tooling.sed_converter.sedml_document import SedMLDocument


class SedCore:
    def __init__(self, sed_files: List[str]) -> None:
        self.files: List[str] = sed_files
        self.parsed_files: Dict[str, SedDocument] = {}

    def validate_all_files(self) -> None:
        for file in self.files:
            print(f"parsing {file}:\n\n\n")
            path: Path = Path(file)
            if path.is_file():
                with path.open("r") as sed:
                    contents = sed.read()
                    self.parsed_files[file] = get_correct_doc(json.loads(contents))
            else:
                print(f"File `{file}` could not be parsed as a file.")

    def convert_to_sedml(self, sed_doc: SedDocument, export_path: str = None) -> SedMLDocument:
        ontologies: list[str] = sed_doc.Metadata.ontologies
        # unsupported ontologies
        if {"pe", "cosim"}.intersection(set(ontologies)):
            raise NotImplementedError(
                "File contains ontologies that can not currently be converted to SedML"
            )
        print("converting Sed to SedML")

    def _combine_sed_documents(self, sed_documents: List[SedDocument]):
        pass  # Not yet implemented
