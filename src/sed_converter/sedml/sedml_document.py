import libsedml
from libsedml import SedAbstractTask as SedMLAbstractTask
from libsedml import SedCurve as SedMLCurve
from libsedml import SedDataGenerator as SedMLDataGenerator
from libsedml import SedDataSet as SedMLDataSet
from libsedml import SedDocument as SedMLDoc
from libsedml import SedError as SedMLError
from libsedml import SedModel as SedMLModel
from libsedml import SedOutput as SedMLOutput
from libsedml import SedParameter as SedMLParameter
from libsedml import SedPlot as SedMLPlot
from libsedml import SedPlot2D as SedMLPlot2D
from libsedml import SedPlot3D as SedMLPlot3D
from libsedml import SedRepeatedTask as SedMLRepeatedTask
from libsedml import SedReport as SedMLReport
from libsedml import SedSimulation as SedMLSimulation
from libsedml import SedSubTask as SedMLSubTask
from libsedml import SedSurface as SedMLSurface
from libsedml import SedTask as SedMLTask
from libsedml import SedVariable as SedMLVariable
from libsedml import XMLNamespaces


class SedMLDocument:
    def __init__(self, file_path: str):
        self.sedml: SedMLDoc = libsedml.readSedML(file_path)
        # Check for errors
        error_count: int = self.sedml.getNumErrors()
        if error_count > 0:
            exception_message: str = f"Found {error_count} errors reading SedML@{file_path}:\n\n"
            for i in range(error_count):
                error: SedMLError = self.sedml.getError(i)
                exception_message += f"\t>({i})> {repr(error)}"
            raise RuntimeError(exception_message)

        # Start pulling from SedML
        self.variables_set: set[SedMLVariable] = set()
        self.parameter_set: set[SedMLParameter] = set()
        self.model_dict: dict[str, SedMLModel] = {}
        self.simulation_dict: dict[str, SedMLSimulation] = {}
        self.task_dict: dict[str, SedMLAbstractTask] = {}
        self.data_gen_dict: dict[str, SedMLDataGenerator] = {}
        self.output_list: list[SedMLOutput] = [
            self.sedml.getOutput(output_index)
            for output_index in range(self.sedml.getNumOutputs())
        ]

        # Start basic parsing
        self._process_document()

    def _process_document(self):
        #  Each call grabs the needed values for the next "call" until we have parsed models and sims.
        self._process_outputs()
        self._process_data_gens()
        self._process_variables_and_params()
        self._process_tasks()

    def _process_outputs(self):
        needed_data_gen_ids: set[str] = set()
        for output in self.output_list:
            if isinstance(output, SedMLPlot):
                if isinstance(output, SedMLPlot2D):
                    for i in range(output.getNumCurves()):
                        curve: SedMLCurve = output.getCurve(i)
                        needed_data_gen_ids.add(curve.getXDataReference())
                        needed_data_gen_ids.add(curve.getYDataReference())
                if isinstance(output, SedMLPlot3D):
                    for i in range(output.getNumSurfaces()):
                        surface: SedMLSurface = output.getSurface(i)
                        needed_data_gen_ids.add(surface.getXDataReference())
                        needed_data_gen_ids.add(surface.getYDataReference())
                        needed_data_gen_ids.add(surface.getZDataReference())
            if isinstance(output, SedMLReport):
                for i in output.getNumDataSets():
                    dataset: SedMLDataSet = output.getDataSet(i)
                    needed_data_gen_ids.add(dataset.getDataReference())

        for data_gen in [self.sedml.getDataGenerator(i)
                         for i in self.sedml.getNumDataGenerators()]:
            data_gen: SedMLDataGenerator = data_gen
            data_gen_id: str = data_gen.getId()
            if data_gen_id in needed_data_gen_ids:
                self.data_gen_dict[data_gen_id] = data_gen

    def _process_data_gens(self):
        for data_gen in list(self.data_gen_dict.values()):
            [self.variables_set.add(data_gen.getVariable(i)) for i in data_gen.getNumVariables()]
            [self.parameter_set.add(data_gen.getParameter(i)) for i in data_gen.getNumParameters()]

    def _process_variables_and_params(self):
        task: SedMLAbstractTask
        needed_task_ids: set[str] = set()
        [needed_task_ids.add(variable.getTaskReference()) for variable in self.variables_set]
        [needed_task_ids.add(parameter.getTaskReference()) for parameter in self.variables_set]
        for task in [self.sedml.getTask(i) for i in range(0, self.sedml.getNumTasks())]:
            if task.getId() in needed_task_ids:
                self.task_dict[task.getId()] = task

    def _process_tasks(self):
        needed_simulation_ids: set[str] = set()
        needed_model_ids: set[str] = set()
        for task in list(self.task_dict.values()):
            if isinstance(task, SedMLTask):
                needed_model_ids.add(task.getModelReference())
                needed_simulation_ids.add(task.getSimulationReference())
            if isinstance(task, SedMLRepeatedTask):
                needed_model_ids, needed_simulation_ids = self.__delve_into_repeated_task(task)
        model: SedMLModel
        sim: SedMLSimulation
        for model in [self.sedml.getModel(i) for i in self.sedml.getNumModels()]:
            self.model_dict[model.getId()] = model
        for sim in [self.sedml.getSimulation(i) for i in self.sedml.getNumSimulations()]:
            self.simulation_dict[sim.getId()] = sim

    def __delve_into_repeated_task(self, repeated_task: SedMLRepeatedTask) \
            -> tuple[set[SedMLModel], set[SedMLSimulation]]:

        model_set: set[SedMLModel] = set()
        sim_set: set[SedMLSimulation] = set()
        subtask: SedMLSubTask
        for subtask in [repeated_task.getSubTask(i) for i in repeated_task.getNumSubTasks()]:
            target_task = self.sedml.getTask(subtask.getTask())  # get task by id
            if isinstance(target_task, SedMLRepeatedTask):
                ret_models, ret_sims = self.__delve_into_repeated_task(target_task)
                model_set.update(ret_models)
                sim_set.update(ret_sims)
            elif isinstance(target_task, SedMLTask):
                model_set.add(target_task.getModelReference())
                sim_set.add(target_task.getSimulationReference())
        return model_set, sim_set

    def export_to_sed(self):
        # Start with Namespaces
        xmlns: XMLNamespaces = self.sedml.getNamespaces()
        for namespace in [xmlns.getPrefix(i) for i in range(0, xmlns.getNumNamespaces())]:
            print(namespace)

