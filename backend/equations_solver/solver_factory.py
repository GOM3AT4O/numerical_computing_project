from typing import Any, Dict

import numpy as np

# Import all solver classes here
from equations_solver.solvers.gauss_elimination_solver import GaussEliminationSolver
from equations_solver.solvers.gauss_jordan_elimination_solver import (
    GaussJordanEliminationSolver,
)
from equations_solver.solvers.gauss_seidel_iteration_solver import (
    GaussSeidelIterationSolver,
)
from equations_solver.solvers.jacobi_iteration_solver import JacobiIterationSolver
from equations_solver.solvers.lu_decomposition_solver import LUDecompositionSolver
from exceptions import ValidationError


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
            number_of_iterations = parameters.get("number_of_iterations", 100)
            absolute_relative_error = parameters.get("absolute_relative_error", 1e-6)
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
            number_of_iterations = parameters.get("number_of_iterations", 100)
            absolute_relative_error = parameters.get("absolute_relative_error", 1e-6)
            return GaussSeidelIterationSolver(
                A,
                b,
                precision,
                initial_guess,
                number_of_iterations,
                absolute_relative_error,
            )

        else:
            raise ValidationError(f"Unknown method: {method}")
