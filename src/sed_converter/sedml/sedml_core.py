from typing import List
from sed_converter.sed.sed_document import SedDocument
from sed_converter.sedml.sedml_document import SedMLDocument


class SedMLCore:
    files: dict[str, SedMLDocument]

    def __int__(self, sedml_files: List[str]) -> None:
        self.files = dict()
        for file in sedml_files:
            self.files[file] = SedMLDocument(file)

    def convert_to_sed(self, file_path: str) -> SedDocument:
        sedml = SedMLDocument(file_path)
        return sedml.export_to_sed()

    def write_to_sedml(self, sed_doc: SedDocument, file_path: str) -> None:
        pass
