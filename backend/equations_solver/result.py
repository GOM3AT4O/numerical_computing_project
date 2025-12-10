import numpy as np
from typing import Dict, List, Optional, Any
from step import Step
from utils import remove_trailing_zeros


class Result:
    solution: Optional[np.ndarray]
    steps: Optional[List[Step]]
    number_of_iterations: Optional[int]
    execution_time: float
    message: str
    L: Optional[np.ndarray]
    U: Optional[np.ndarray]
    P: Optional[np.ndarray]

    def __init__(
        self,
        solution: Optional[np.ndarray] = None,
        steps: Optional[List[Step]] = None,
        iterations_steps: Optional[List[str]] = None,
        number_of_iterations: Optional[int] = None,
        execution_time: float = 0.0,
        message: str = "Solution found",
    ):
        self.solution = solution
        self.steps = steps
        self.number_of_iterations = number_of_iterations
        self.execution_time = execution_time
        self.message = message
        self.iterations_steps = iterations_steps

        # optional fields for LU decomposition
        self.L = None
        self.U = None
        self.P = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "message": self.message,
            "execution_time": round(self.execution_time, 12),
        }

        if self.solution is not None:
            result["solution"] = np.vectorize(remove_trailing_zeros)(
                self.solution
            ).tolist()

        if self.steps is not None:
            result["steps"] = [step.to_dict() for step in self.steps]

        if self.iterations_steps is not None:
            result["iterations_steps"] = self.iterations_steps

        if self.number_of_iterations is not None:
            result["number_of_iterations"] = self.number_of_iterations

        if self.L is not None:
            result["L"] = np.vectorize(remove_trailing_zeros)(self.L).tolist()

        if self.U is not None:
            result["U"] = np.vectorize(remove_trailing_zeros)(self.U).tolist()

        if self.P is not None:
            result["P"] = np.vectorize(remove_trailing_zeros)(self.P).tolist()

        return result
