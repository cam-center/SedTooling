from sed_model.simulation import Simulation


class UniformTimeCourse(Simulation):
    num_of_points: float
    end_time: float
    start_time: float
    output_start_time: float

    def __init__(
        self,
        algorithm: str,
        num_of_points: float,
        end_time: float,
        start_time: float = 0.0,
        output_start_time: float = 0.0,
    ):
        super().__init__(algorithm)
        self.start_time = start_time
        self.end_time = end_time
        self.output_start_time = output_start_time
        self.num_of_points = num_of_points
