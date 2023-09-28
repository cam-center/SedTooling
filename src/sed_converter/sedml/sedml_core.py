import re
from re import Match
from typing import Union

from sed_converter.sed.sed_document import SedDocument
from sed_converter.sedml.sedml_document import SedMLDocument
from sed_converter.actions.action import Action
from sed_converter.actions.load.load import Load
from sed_converter.declarations.variables.variable import Variable
from sed_converter.dependencies.dependency import Dependency
from sed_converter.metadata.metadata import Metadata
from sed_converter.declarations.declarations import Declarations

from libsedml import XMLNamespaces
from libsedml import SedModel as SedMLModel
from libsedml import SedSimulation as SedMLSimulation
from libsedml import SedAbstractTask as SedMLAbstractTask
from libsedml import SedSubTask as SedMLSubTask
from libsedml import SedTask as SedMLTask
from libsedml import SedSurface as SedMLSurface


class SedMLCore:
    def __init__(self, sedml_files: list[str]):
        self.files: list[str] = sedml_files
        self.parsed_files: dict[str, SedMLDocument] = {}

    def validate_all_files(self):
        for file in self.files:
            print(f"parsing {file}:\n\n\n")
            self.parsed_files[file] = SedMLDocument(file)

    def convert_all_to_sed(self, export: bool = False):
        sed_docs: list[SedDocument] = []
        for filepath in self.parsed_files.keys():
            if export:
                sed_docs.append(self.convert_to_sed(self.parsed_files[filepath],
                                                    filepath.replace(".sedml", ".sed")))
            else:
                sed_docs.append(self.convert_to_sed(self.parsed_files[filepath]))

    @classmethod
    def convert_to_sed(cls, sedml_doc: SedMLDocument, export_path: str = None) -> SedDocument:
        proto_sed: dict[str, Union[Metadata, list, dict[str, list]]] = {
            "Metadata": None,
            "Dependencies": [],
            "Declarations": {"Constants": [], "Variables": []},
            "Actions": [],
            "Inputs": [],
            "Outputs": []
        }
        variables: list[dict] = []
        ontologies: list[str] = ["KiSAO"]
        # Start with Namespaces
        xmlns: XMLNamespaces = sedml_doc.sedml.getNamespaces()
        for namespace in [xmlns.getPrefix(i) for i in range(0, xmlns.getNumNamespaces())]:
            namespace: str
            if namespace == "sbml":
                sbml_level: int = -1
                sbml_version: int = -1
                separator = ("/" if "/" in namespace else "\\")
                for part in namespace.split(separator):
                    if "level" in part:
                        sbml_level = int(part[-1])
                    if "version" in part:
                        sbml_version = int(part[-1])
                if sbml_level == -1 and sbml_version == -1:
                    raise ValueError(f"Unable to determine level and version of sbml.")
                if sbml_level == -1 or sbml_version == -1:
                    raise ValueError(f"Unable to determine {'level' if sbml_level < 0 else 'version'} of sbml")
                ontologies.append(f"sbml<{sbml_level},{sbml_version}>")

        # Then Models
        cls._convert_models(proto_sed, list(sedml_doc.model_dict.values()))
        cls._convert_sims(proto_sed, list(sedml_doc.simulation_dict.values()), list(sedml_doc.task_dict.values()))

    @classmethod
    def _convert_models(cls, proto_sed: dict[str, Union[Metadata, list, dict[str, list]]],
                        models: list[SedMLModel]) -> list[dict]:
        variables_to_return: list[dict] = []
        for model in models:
            if "language:sbml" in model.getLanguage():
                # Add Dependency
                proto_sed["Dependencies"].append(
                    Dependency(name=f"Dependency: `{model.getName()}`", identifier=f"dep_{model.getId()}",
                               type=f"sbml::SBMLFile", source=f"{model.getSource()}"))

                # "Add" Variable
                variables_to_return.append(
                    {"name": f"{model.getName()}", "identifier": f"{model.getId()}",
                     "type": f"Model<sbml::SBMLFile>", "bindings": {}})

                # Add Load Action
                proto_sed["Actions"].append(Load(name=f"Load Model: {model.getId()}",
                                                 identifier=f"load_{model.getId()}", type=f"sbml::load_sbml",
                                                 source=f"dep_{model.getId()}", target=f"{model.getId()}"))
            else:
                raise ValueError("Unknown type of model was attempted to be parsed. "
                                 "Only SBML is supported at this time.")

        return variables_to_return

    @classmethod
    def _convert_sims(cls, proto_sed: dict[str, Union[Metadata, list, dict[str, list]]],
                      sims: list[SedMLSimulation], tasks: list[SedMLAbstractTask]) -> list[dict]:
        variables_to_return: list[dict] = []
        for task in tasks:
            if isinstance(task, SedMLTask):
                
        return variables_to_return


