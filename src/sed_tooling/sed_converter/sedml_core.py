import re
from re import Match
from typing import Union

import libsedml

from sed_tooling.sed_model.sed_document import SedDocument
from sed_tooling.sed_converter.sedml_document import SedMLDocument
from sed_tooling.sed_model.load_action import Load
from sed_tooling.sed_model.dependency import Dependency
from sed_tooling.sed_model.metadata import Metadata
from sed_tooling.sed_model.simulation import LoopedSimulation
from sed_tooling.sed_model.constant import Constant
from sed_tooling.sed_model.variable import Variable, BasicVariable, Model, ModelElementReference
from sed_tooling.sed_model.uniform_time_course import (
    UniformTimeCourseSim,
    UniformTimeCourseSimSpatial,
)
from sed_tooling.sed_model.steady_state import (
    SteadyStateSim,
    SteadyStateSimSpatial,
)
from sed_tooling.sed_model.one_step import (
    OneStepSim,
    OneStepSimSpatial,
)


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
from libsedml import SedAlgorithm as SedMLAlgorithm
from libsedml import SedAlgorithmParameter as SedMLAlgorithmParameter
from libsedml import SedVariable as SedMLVariable
from libsedml import SedParameter as SedMLParameter
from libsedml import SedDataGenerator as SedMLDataGenerator
from libsedml import ASTNode
from libsedml import formulaToL3String


class SedMLCore:
    _spatial_algorithm_kisao_terms: set[str] = {
        "KISAO:0000021",  # StochSim nearest-neighbour algorithm
        "KISAO:0000057",  # Brownian diffusion Smoluchowski method
        "KISAO:0000058",  # Greens function reaction dynamics (GFRD)
        "KISAO:0000075",  # Gillespie multi-particle method
        "KISAO:0000095",  # sub-volume stochastic reaction-diffusion algorithm
        "KISAO:0000264",  # cellular automata update method
        "KISAO:0000273",  # hard-particle molecular dynamics
        "KISAO:0000274",  # first-passage Monte Carlo algorithm
        "KISAO:0000278",  # Metropolis Monte Carlo algorithm
        "KISAO:0000285",  # finite volume method
        "KISAO:0000306",  # Lagrangian sliding fluid element algorithm
        "KISAO:0000307",  # finite difference method
        "KISAO:0000308",  # MacCormack method
        "KISAO:0000309",  # Crank-Nicolson method
        "KISAO:0000309",  # method of lines
        "KISAO:0000316",  # enhanced Greens function reaction dynamics (enhanced GFRD)
        "KISAO_0000337",  # finite element method
        "KISAO_0000338",  # h-version of the finite element method
        "KISAO_0000339",  # p-version of the finite element method
        "KISAO_0000340",  # h-p version of the finite element method
        "KISAO_0000341",  # mixed finite element method
        "KISAO_0000342",  # level set method
        "KISAO_0000343",  # generalized finite element method
        "KISAO_0000345",  # h-p cloud method
        "KISAO_0000348",  # extended finite element method
        "KISAO_0000349",  # method of finite spheres
        "KISAO:0000369",  # partial differential equation discretization method
        "KISAO:0000582",  # Spatiocyte method
        "KISAO:0000615",  # fully-implicit regular grid finite volume method with a variable time step
        "KISAO_0000616",  # semi-implicit regular grid finite volume method with a fixed time step
    }

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
        vars_and_consts: dict[str, Union[Variable, Constant]] = {}
        ontologies: list[str] = ["sed", "KiSAO"]
        # Start with Namespaces
        xmlns: XMLNamespaces = sedml_doc.sedml.getNamespaces()
        for namespace in [xmlns.getPrefix(i) for i in range(xmlns.getNumNamespaces())]:
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

            if namespace == "spatial":
                ontologies.append("sim<spatial>")

        # Then Models
        cls._convert_models(
            proto_sed, list(sedml_doc.model_dict.values()), ontologies, vars_and_consts
        )

        # Then simulations / Tasks
        cls._convert_sims(
            proto_sed,
            list(sedml_doc.simulation_dict.values()),
            list(sedml_doc.task_dict.values()),
            vars_and_consts,
        )

    @classmethod
    def _convert_vars_params_math_and_ontologies(
        cls, sedmlDoc: SedMLDocument, proto_sed: dict[str, Union[Metadata, list, dict[str, list]]]
    ):
        # Models
        for model_id in sedmlDoc.model_dict:
            if sedmlDoc.model_dict[model_id].getId() not in proto_sed["Declarations"]["Variables"]:
                if not re.match("language.sbml", sedmlDoc.model_dict[model_id].getLanguage()):
                    raise TypeError("Non-sbml models are unsupported at this time.")

                proto_sed["Declarations"]["Variables"].append(
                    Model(
                        name=f"{sedmlDoc.model_dict[model_id].getName()}",
                        identifier=f"{sedmlDoc.model_dict[model_id].getId()}",
                        type=f"modeling::Model<sbml::SBMLFile>",
                        bindings={"Time": "sed::TIME"},
                    )
                )
        # Sims

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    @classmethod
    def _convert_models(
        cls,
        proto_sed: dict[str, Union[Metadata, list, dict[str, list]]],
        models: list[SedMLModel],
        ontologies: list[str],
        vars_and_consts: dict[str, Union[Variable, Constant]],
    ) -> list[dict]:
        variables_to_return: list[dict] = []
        for model in models:
            if "language:sbml" in model.getLanguage():
                if "modeling" not in ontologies:
                    ontologies.append("modeling")
                if "sbml" not in ontologies:
                    ontologies.append("sbml")

                # Add Dependency
                proto_sed["Dependencies"].append(
                    Dependency(
                        name=f"Dependency: `{model.getName()}`",
                        identifier=f"dep_{model.getId()}",
                        type=f"sbml::SBMLFile",
                        source=f"{model.getSource()}",
                    )
                )

                # "Add" Variable (we'll add all variables and constants at the end
                if model.getId() not in vars_and_consts:
                    vars_and_consts[model.getId()] = Model(
                        name=f"{model.getName()}",
                        identifier=f"{model.getId()}",
                        type=f"modeling::Model<sbml::SBMLFile>",
                        bindings={"Time": "sed::TIME"},
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
        vars_and_consts: dict[str, Union[Variable, Constant]],
    ):
        normal_tasks: list
        for task in tasks:
            current_task: Union[SedMLTask, SedMLRepeatedTask, SedMLAbstractTask] = task
            preprocess_task: SedMLAbstractTask = current_task
            while isinstance(preprocess_task, SedMLRepeatedTask):
                for tsk in tasks:
                    if tsk.getId() == preprocess_task.getSubTask(0):
                        preprocess_task = tsk
            if not isinstance(preprocess_task, SedMLTask):
                raise NotImplementedError(
                    "Only Repeated and normal Tasks are implemented at this time."
                )
            preprocess_task: SedMLTask
            base_model_id = preprocess_task.getModelReference()

            while isinstance(current_task, SedMLRepeatedTask):
                # Process ranges
                sed_range: SedMLRange
                for sed_range in [
                    current_task.getRange(i) for i in range(current_task.getNumRanges())
                ]:
                    assert not isinstance(sed_range, SedMLDataRange)
                    assert not isinstance(sed_range, SedMLFunctionalRange)

                    if isinstance(sed_range, SedMLVectorRange):
                        vector: list[str] = [str(float(elem)) for elem in sed_range.getValues()]
                        vector_range = f'[{", ".join(vector)}]'
                        if sed_range.getId() not in vars_and_consts:
                            vars_and_consts[sed_range.getId()] = Constant(
                                name=f"{sed_range.getName()}",
                                identifier=f"{sed_range.getId()}",
                                type=f"sed::vector",
                                value=f"{vector_range}",
                            )
                    elif isinstance(sed_range, SedMLUniformRange):
                        start: float = float(sed_range.getStart())
                        end: float = float(sed_range.getEnd())
                        step_size: float = (end - start) / float(sed_range.getNumberOfSteps())
                        uniform_range = f"({start}, {end}, {step_size})"
                        if sed_range.getId() not in vars_and_consts:
                            vars_and_consts[sed_range.getId()] = Constant(
                                name=f"{sed_range.getName()}",
                                identifier=f"{sed_range.getId()}",
                                type=f"sed::range",
                                value=f"{uniform_range}",
                            )

                    else:
                        raise ValueError("Unknown range type encountered")

                # Process changes
                override_dict: dict[str, str] = {}
                change: SedMLSetValue
                for change in [
                    current_task.getTaskChange(i) for i in range(current_task.getNumTaskChanges())
                ]:
                    node: ASTNode = change.getMath()
                    str_repr: str = str(libsedml.formulaToL3String(node))
                    var: SedMLVariable
                    for var in [change.getVariable(i) for i in range(change.getNumVariables())]:
                        targeted_value: str = var.getSymbol()
                        if targeted_value is None or targeted_value == "":
                            # No symbol, so there's a target instead
                            targeted_value = var.getTarget()
                        if var.getId() not in vars_and_consts:
                            if re.fullmatch("/(\w:\w/)*\[@i\w='\w']", targeted_value):
                                # It's a model reference
                                str_repr.replace(
                                    f"{var.getId()}",
                                    f"$model.{var.getId()}",
                                )
                                vars_and_consts[base_model_id].bindings[
                                    str(var.getId())
                                ] = targeted_value
                            else:
                                vars_and_consts[var.getId()] = BasicVariable(
                                    name=f"{var.getName()}",
                                    identifier=f"{var.getId()}",
                                    type=f"sed::basicVariable",
                                    source=f"{targeted_value}",
                                )

                    for const in [
                        change.getParameter(i) for i in range(change.getNumParameters())
                    ]:
                        const: SedMLParameter
                        if const.getId() not in vars_and_consts:
                            vars_and_consts[const.getId()] = Constant(
                                name=f"{const.getName()}",
                                identifier=f"{const.getId()}",
                                type=f"sed::basicVariable",
                                value=f"{float(const.getValue())}",
                            )
                    # apply change
                    vars_and_consts[base_model_id].bindings[str(change.getId())] = str(
                        change.getTarget()
                    )
                    override_dict[str(change.getId())] = str_repr

                # Add a looped sim task
                proto_sed["Actions"].append(
                    LoopedSimulation(
                        name=f"{current_task.getName()}",
                        identifier=f"{current_task.getId()}",
                        type=f"sim::LoopedSimulation",
                        sim=f"{[current_task.getSubTask(i) for i in range(current_task.getNumSubTasks())]}",
                        modelReset=bool(current_task.getResetModel()),
                        parameterScan=bool(False),
                        overrides=override_dict,
                    )
                )

                # iterate to next task
                for tsk in tasks:
                    if tsk.getId() == current_task.getSubTask(0):
                        current_task = tsk
                # end while loop

            # Add normal task
            current_task: SedMLTask
            for sim in sims:
                if sim.getId() == current_task.getSimulationReference():
                    alg: SedMLAlgorithm = sim.getAlgorithm()
                    alg_params: list[SedMLAlgorithmParameter] = [
                        alg.getAlgorithmParameter(i)
                        for i in range(alg.getNumAlgorithmParameters())
                    ]
                    is_spatial: bool = (
                        True if alg.getKisaoID() in cls._spatial_algorithm_kisao_terms else False
                    )
                    if isinstance(sim, SedMLAnalysis):
                        raise NotImplementedError("SedML Analysis not yet supported")
                    if isinstance(sim, SedMLUniformTimeCourse):
                        if is_spatial:
                            proto_sed["Actions"].append(
                                UniformTimeCourseSimSpatial(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::SpatialSimulation<UTC>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                    numDataPoints=int(sim.getNumberOfPoints()),
                                    endTime=float(sim.getOutputEndTime()),
                                    startTime=float(sim.getInitialTime()),
                                    outputStartTime=float(sim.getOutputStartTime()),
                                )
                            )
                        else:
                            proto_sed["Actions"].append(
                                UniformTimeCourseSim(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::NonspatialSimulation<UTC>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                    numDataPoints=int(sim.getNumberOfPoints()),
                                    endTime=float(sim.getOutputEndTime()),
                                    startTime=float(sim.getInitialTime()),
                                    outputStartTime=float(sim.getOutputStartTime()),
                                )
                            )
                    if isinstance(sim, SedMLSteadyState):
                        if is_spatial:
                            proto_sed["Actions"].append(
                                SteadyStateSimSpatial(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::SpatialSimulation<SteadyState>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                )
                            )
                        else:
                            proto_sed["Actions"].append(
                                SteadyStateSim(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::NonspatialSimulation<SteadyState>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                )
                            )
                    if isinstance(sim, SedMLOneStep):
                        if is_spatial:
                            proto_sed["Actions"].append(
                                OneStepSimSpatial(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::SpatialSimulation<OneStep>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                )
                            )
                        else:
                            proto_sed["Actions"].append(
                                OneStepSim(
                                    name=f"{current_task.getName()}({sim.getName()})",
                                    identifier=f"{current_task.getId()}",
                                    type="sim::NonspatialSimulation<OneStep>",
                                    algorithm=f"{alg.getKisaoID()}",
                                    algorithmParameters={
                                        param.getKisaoID(): param.getValue()
                                        for param in alg_params
                                    },
                                )
                            )
        return

    @classmethod
    def _convert_data_gens(
        cls,
        proto_sed: dict[str, Union[Metadata, list, dict[str, list]]],
        data_gens: list[SedMLDataGenerator],
        ontologies: list[str],
        vars_and_consts: dict[str, Union[Variable, Constant]],
    ):
        for data_gen in data_gens:
            equation: str = data_gen.getMath()
