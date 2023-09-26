import libsedml

from sed_converter.Sed.SedDocument import SedDocument
from typing import Union

from libsedml import SedError as SedMLError
from libsedml import SedDocument as SedMLDoc

from libsedml import SedModel as SedMLModel
from libsedml import SedSimulation as SedMLSimulation
from libsedml import SedAbstractTask as SedMLAbstractTask
from libsedml import SedDataGenerator as SedMLDataGenerator
from libsedml import SedOutput as SedMLOutput
from libsedml import SedPlot as SedMLPlot
from libsedml import SedPlot2D as SedMLPlot2D
from libsedml import SedPlot3D as SedMLPlot3D
from libsedml import SedReport as SedMLReport
from libsedml import SedCurve as SedMLCurve
from libsedml import SedSurface as SedMLSurface
from libsedml import SedDataSet as SedMLDataSet


class SedMLDocument:

    def __init__(self, file_path: str):
        self.sedml: SedMLDoc = libsedml.readSedML(file_path)
        # Check for errors
        error_count: int = self.sedml.getNumErrors()
        if error_count > 0:
            exception_message: str = f"Found {error_count} errors reading SedML@{file_path}:\n\n"
            for i in range(0, error_count):
                error: SedMLError = self.sedml.getError(i)
                exception_message += f"\t>({i})> {repr(error)}"
            raise RuntimeError(exception_message)

        # Start pulling from SedML
        self.model_dict: dict[str, SedMLModel] = {}
        self.simulation_dict: dict[str, SedMLSimulation] = {}
        self.task_dict: dict[str, SedMLAbstractTask] = {}
        self.data_gen_dict: dict[str, SedMLDataGenerator] = {}
        self.output_list: list[SedMLOutput] = \
            [self.sedml.getOutput(output_index) for output_index in range(0, self.sedml.getNumOutputs())]
        self._processDocument()

    def _processDocument(self):
        self._processOutputs()

    def _processOutputs(self):
        needed_data_gen_ids: set[str] = set()
        for output in self.output_list:
            if isinstance(output, SedMLPlot):
                plot: SedMLPlot = output
                if isinstance(plot, SedMLPlot2D):
                    plot2: SedMLPlot2D = plot
                    for i in range(0, plot2.getNumCurves()):
                        curve: SedMLCurve = plot2.getCurve(i)
                        needed_data_gen_ids.add(curve.getXDataReference())
                        needed_data_gen_ids.add(curve.getYDataReference())
                if isinstance(plot, SedMLPlot3D):
                    plot3: SedMLPlot3D = plot
                    for i in range(0, plot3.getNumSurfaces()):
                        surface: SedMLSurface = plot3.getSurface(i)
                        needed_data_gen_ids.add(surface.getXDataReference())
                        needed_data_gen_ids.add(surface.getYDataReference())
                        needed_data_gen_ids.add(surface.getZDataReference())
            if isinstance(output, SedMLReport):
                report: SedMLReport = output
                for i in report.getNumDataSets():
                    dataset: SedMLDataSet = report.getDataSet(i)
                    needed_data_gen_ids.add(dataset.getDataReference())

        for data_gen in [self.sedml.getDataGenerator(i) for i in self.sedml.getNumDataGenerators()]:
            data_gen: SedMLDataGenerator = data_gen
            data_gen_id: str = data_gen.getId()
            if data_gen_id in needed_data_gen_ids:
                self.data_gen_dict[data_gen_id] = data_gen

    def _processDataGens(self):
        data_gens = list(self.data_gen_dict.values())
        for data_gen in data_gens:
            data_gen

    def exportToSed(self):
        pass

