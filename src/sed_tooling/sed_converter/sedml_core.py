import re
from re import Match
from typing import Union

from sed_tooling.sed_model.sed_document import SedDocument
from sed_tooling.sed_converter.sedml_document import SedMLDocument
from sed_tooling.sed_model.load_action import Load
from sed_tooling.sed_model.dependency import Dependency
from sed_tooling.sed_model.metadata import Metadata
from sed_tooling.sed_model.simulation import LoopedSimulation
from sed_tooling.sed_model.constant import Constant
from sed_tooling.sed_model.uniform_time_course import UniformTimeCourseSim, UniformTimeCourseSimSpatial


from libsedml import XMLNamespaces
from libsedml import SedModel as SedMLModel
from libsedml import SedSimulation as SedMLSimulation
from libsedml import SedUniformTimeCourse as SedMLUniformTimeCourse
from libsedml import SedSteadyState as SedMLSteadyState
from libsedml import SedOneStep as SedMLOneStep
from libsedml import SedAnalysis as SedMLAnalysis
from libsedml import SedAbstractTask as SedMLAbstractTask
from libsedml import SedTask as SedMLTask
from libsedml import SedRepeatedTask as SedMLRepeatedTask
from libsedml import SedSetValue as SedMLSetValue
from libsedml import SedRange as SedMLRange
from libsedml import SedFunctionalRange as SedMLFunctionalRange
from libsedml import SedDataRange as SedMLDataRange
from libsedml import SedUniformRange as SedMLUniformRange
from libsedml import SedVectorRange as SedMLVectorRange
from libsedml import ASTNode


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
                sed_docs.append(
                    self.convert_to_sed(
                        self.parsed_files[filepath], filepath.replace(".sedml", ".sed")
                    )
                )
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
            "Outputs": [],
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
                separator = "/" if "/" in namespace else "\\"
                for part in namespace.split(separator):
                    if "level" in part:
                        sbml_level = int(part[-1])
                    if "version" in part:
                        sbml_version = int(part[-1])
                if sbml_level == -1 and sbml_version == -1:
                    raise ValueError(f"Unable to determine level and version of sbml.")
                if sbml_level == -1 or sbml_version == -1:
                    raise ValueError(
                        f"Unable to determine {'level' if sbml_level < 0 else 'version'} of sbml"
                    )
                ontologies.append(f"sbml<{sbml_level},{sbml_version}>")

        # Then Models
        cls._convert_models(proto_sed, list(sedml_doc.model_dict.values()))
        cls._convert_sims(
            proto_sed, list(sedml_doc.simulation_dict.values()), list(sedml_doc.task_dict.values())
        )

    @classmethod
    def _convert_models(
        cls, proto_sed: dict[str, Union[Metadata, list, dict[str, list]]], models: list[SedMLModel]
    ) -> list[dict]:
        variables_to_return: list[dict] = []
        for model in models:
            if "language:sbml" in model.getLanguage():
                # Add Dependency
                proto_sed["Dependencies"].append(
                    Dependency(
                        name=f"Dependency: `{model.getName()}`",
                        identifier=f"dep_{model.getId()}",
                        type=f"sbml::SBMLFile",
                        source=f"{model.getSource()}",
                    )
                )

                # "Add" Variable
                variables_to_return.append(
                    {
                        "name": f"{model.getName()}",
                        "identifier": f"{model.getId()}",
                        "type": f"Model<sbml::SBMLFile>",
                        "bindings": {},
                    }
                )

                # Add Load Action
                proto_sed["Actions"].append(
                    Load(
                        name=f"Load Model: {model.getId()}",
                        identifier=f"load_{model.getId()}",
                        type=f"sbml::load_sbml",
                        source=f"dep_{model.getId()}",
                        target=f"{model.getId()}",
                    )
                )
            else:
                raise ValueError(
                    "Unknown type of model was attempted to be parsed. "
                    "Only SBML is supported at this time."
                )

        return variables_to_return

    @classmethod
    def _convert_sims(
        cls,
        proto_sed: dict[str, Union[Metadata, list, dict[str, list]]],
        sims: list[SedMLSimulation],
        tasks: list[SedMLAbstractTask],
    ) -> list[dict]:
        processed_task_ids: set[str] = set()
        variables_to_return: list[dict] = []
        normal_tasks: list
        for task in tasks:
            current_task = task
            while isinstance(current_task, SedMLRepeatedTask):
                # Process ranges
                range: SedMLRange
                for range in [current_task.getRange(i) for i in current_task.getNumRanges()]:
                    assert not isinstance(range, SedMLDataRange)
                    assert not isinstance(range, SedMLFunctionalRange)

                    if isinstance(range, SedMLVectorRange):
                        vector: list[str] = [str(float(elem)) for elem in range.getValues()]
                        sed_range = f'[{", ".join(vector)}]'
                        proto_sed["Declarations"]["Constants"].append(
                            Constant(
                                name=f"{range.getName()}",
                                identifier=f"{range.getId()}",
                                type=f"sed::vector",
                                value=f"{sed_range}",
                            )
                        )
                    elif isinstance(range, SedMLUniformRange):
                        start: float = float(range.getStart())
                        end: float = float(range.getEnd())
                        step_size: float = (end - start) / float(range.getNumberOfSteps())
                        sed_range = f"({start}, {end}, {step_size})"
                        proto_sed["Declarations"]["Constants"].append(
                            Constant(
                                name=f"{range.getName()}",
                                identifier=f"{range.getId()}",
                                type=f"sed::range",
                                value=f"{sed_range}",
                            )
                        )
                    else:
                        raise ValueError("Unknown range type encountered")

                # Process changes
                change: SedMLSetValue
                for change in [
                    current_task.getTaskChange(i) for i in current_task.getNumTaskChanges()
                ]:
                    math: ASTNode
                    for math in change.getMath():
                        math.getListOfNodes()
                        raise NotImplementedError("MathML parsing not implemented yet")
                    for var in [change.getVariable(i) for i in change.getNumVariables()]:
                        pass

                # Add a looped sim task
                proto_sed["Actions"].append(
                    LoopedSimulation(
                        name=f"",
                        identifier=f"",
                        type=f"",
                        sim=f"",
                        modelReset=bool(current_task.getResetModel()),
                        parameterScan=bool(),
                        overrides={},
                    )
                )
            if not isinstance(current_task, SedMLTask):
                raise NotImplementedError(
                    "Only Repeated and normal Tasks are implemented at this time."
                )

            # Add normal task

            for sim in sims:
                if sim.getId() == current_task.getSimulationReference():
                    if isinstance(sim, SedMLAnalysis):
                        raise NotImplementedError("SedML Analysis not yet supported")
                    if isinstance(sim, SedMLUniformTimeCourse):
                        proto_sed["Actions"].append(

                        )

        return variables_to_return
