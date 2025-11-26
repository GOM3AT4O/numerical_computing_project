from typing import Any, Dict
import numpy as np
from utils import remove_trailing_zeros
from step import Step


class Iteration(Step):
    iteration_type: str
    matrix: np.ndarray
    old_solution: np.ndarray
    new_solution: np.ndarray

    def __init__(
        self,
        iteration_type: str,
        matrix: np.ndarray,
        old_solution: np.ndarray,
        new_solution: np.ndarray,
    ):
        super().__init__("iteration")

        self.iteration_type = iteration_type
        self.matrix = matrix
        self.old_solution = old_solution
        self.new_solution = new_solution

    @classmethod
    def jacobi(
        cls, matrix: np.ndarray, old_solution: np.ndarray, new_solution: np.ndarray
    ) -> "Iteration":
        return cls(
            iteration_type="jacobi",
            matrix=matrix,
            old_solution=old_solution,
            new_solution=new_solution,
        )

    @classmethod
    def gauss_seidel(
        cls, matrix: np.ndarray, old_solution: np.ndarray, new_solution: np.ndarray
    ) -> "Iteration":
        return cls(
            iteration_type="gauss-seidel",
            matrix=matrix,
            old_solution=old_solution,
            new_solution=new_solution,
        )

    def to_dict(self) -> Dict[str, Any]:
        solution = {
            "step_type": self.step_type,
            "iteration_type": self.iteration_type,
            "matrix": np.vectorize(remove_trailing_zeros)(self.matrix).tolist(),
            "old_solution": np.vectorize(remove_trailing_zeros)(
                self.old_solution
            ).tolist(),
            "new_solution": np.vectorize(remove_trailing_zeros)(
                self.new_solution
            ).tolist(),
        }

        return solution
