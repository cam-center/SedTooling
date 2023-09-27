from sed_converter.ontologies.simulation.simulation import Simulation


class UniformTimeCourse(Simulation):
    def __init__(
        self, algorithm, num_of_points, end_time, start_time=0, output_start_time=0
    ) -> None:
        super(algorithm)
        self.start_time = start_time
        self.end_time = end_time
        self.output_start_time = output_start_time
        self.num_of_points = num_of_points
