import libsedml

from sed_converter.Sed.SedDocument import SedDocument
from sed_converter.SedML.SedMLDocument import SedMLDocument


class SedMLCore:

    def __int__(self, sedml_files: list[str]):
        self.files: dict[str, SedMLDocument] = {}
        for file in sedml_files:
            self.files[file] = SedMLDocument(file)

    def convertToSed(self, file_path: str) -> SedDocument:
        sedml = SedMLDocument(file_path)
        return sedml.exportToSed()


    def writeOutToSedML(self, sed_doc: SedDocument, file_path: str) -> None:
        pass
