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
    def create_solver(method: str, A: np.ndarray, b: np.ndarray, 
                     precision: int, params: Dict[str, Any]):
        

        method = method.lower().replace(" ", "").replace("-", "")

        if method == "gausselimination":
            return GaussEliminationSolver(A, b, precision)
        
        elif method == "gaussjordan":
            return GaussJordanSolver(A, b, precision)
        
        elif method== "ludecomposition":
            form= params.get('form','doolittle').lower()
            return LUDecompositionSolver(A, b, precision, form)
        
        elif method=="jacobi":
            initial_guess = params.get('initial_guess')
            max_iterations= params.get('max_iterations')
            tolerance =params.get('tolerance')
            return JacobiSolver(A, b, precision, initial_guess, max_iterations, tolerance)
        
        elif method == "gaussseidel":
            initial_guess = params.get('initial_guess')
            max_iterations = params.get('max_iterations')
            tolerance = params.get('tolerance')
            return GaussSeidelSolver(A, b, precision, initial_guess, max_iterations, tolerance)
        
        else:
            raise ValidationError(f"Unknown method:{method}")
        
        