from sed_converter.sed.sed_document import SedDocument
from sed_converter.sedml.sedml_document import SedMLDocument


class SedMLCore:
    def __int__(self, sedml_files: list[str]):
        self.files: dict[str, SedMLDocument] = {}
        for file in sedml_files:
            self.files[file] = SedMLDocument(file)

    def convert_to_sed(self, file_path: str) -> SedDocument:
        sedml = SedMLDocument(file_path)
        return sedml.export_to_sed()

    def write_to_sedml(self, sed_doc: SedDocument, file_path: str) -> None:
        pass
