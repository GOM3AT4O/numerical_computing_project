import numpy as np
from typing import Dict, Any
from exceptions import ValidationError
from solvers.gauss_elimination_solver import GaussEliminationSolver
from solvers.gauss_jordan_elimination_solver import GaussJordanEliminationSolver
from solvers.lu_decomposition_solver import LUDecompositionSolver
from solvers.jacobi_iteration_solver import JacobiIterationSolver
from solvers.gauss_seidel_iteration_solver import GaussSeidelIterationSolver


class SolverFactory:
    @staticmethod
    def create_solver(
        method: str,
        A: np.ndarray,
        b: np.ndarray,
        precision: int,
        parameters: Dict[str, Any],
    ):
        if method == "gauss-elimination":
            scaling = parameters.get("scaling", False)
            return GaussEliminationSolver(A, b, precision, scaling)

        elif method == "gauss-jordan-elimination":
            scaling = parameters.get("scaling", False)
            return GaussJordanEliminationSolver(A, b, precision, scaling)

        elif method == "lu-decomposition":
            format = parameters.get("format", "doolittle").lower()
            return LUDecompositionSolver(A, b, precision, format)

        elif method == "jacobi-iteration":
            initial_guess = parameters.get("initial_guess")
            number_of_iterations = parameters.get("number_of_iterations")
            absolute_relative_error = parameters.get("absolute_relative_error")
            return JacobiIterationSolver(
                A,
                b,
                precision,
                initial_guess,
                number_of_iterations,
                absolute_relative_error,
            )

        elif method == "gauss-seidel-iteration":
            initial_guess = parameters.get("initial_guess")
            number_of_iterations = parameters.get("number_of_iterations")
            absolute_relative_error = parameters.get("absolute_relative_error")
            return GaussSeidelIterationSolver(
                A,
                b,
                precision,
                initial_guess,
                number_of_iterations,
                absolute_relative_error,
            )

        else:
            raise ValidationError(f"Unknown method:{method}")
