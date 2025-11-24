import numpy as np
from typing import Dict, Any
from exceptions import ValidationError
from gauss_elimination import GaussEliminationSolver
from gauss_jordan import GaussJordanSolver
from lu_decomposition import LUDecompositionSolver
from jacobi import JacobiSolver
from gauss_seidel import GaussSeidelSolver


class SolverFactory:
    @staticmethod
    def create_solver(
        method: str,
        A: np.ndarray,
        b: np.ndarray,
        precision: int,
        params: Dict[str, Any],
    ):
        if method == "gauss-elimination":
            return GaussEliminationSolver(A, b, precision)

        elif method == "gauss-jordan-elimination":
            return GaussJordanSolver(A, b, precision)

        elif method == "lu-decomposition":
            format = params.get("format", "doolittle").lower()
            return LUDecompositionSolver(A, b, precision, format)

        elif method == "jacobi-iteration":
            initial_guess = params.get("initial_guess")
            number_of_iterations = params.get("number_of_iterations")
            absolute_relative_error = params.get("absolute_relative_error")
            return JacobiSolver(
                A,
                b,
                precision,
                initial_guess,
                number_of_iterations,
                absolute_relative_error,
            )

        elif method == "gauss-seidel-iteration":
            initial_guess = params.get("initial_guess")
            number_of_iterations = params.get("number_of_iterations")
            absolute_relative_error = params.get("absolute_relative_error")
            return GaussSeidelSolver(
                A,
                b,
                precision,
                initial_guess,
                number_of_iterations,
                absolute_relative_error,
            )

        else:
            raise ValidationError(f"Unknown method:{method}")
