from sed_tooling.sed_model.simulation import Simulation


class SteadyState(Simulation):
    def __init__(self, algorithm: str) -> None:
        super().__init__(algorithm)
