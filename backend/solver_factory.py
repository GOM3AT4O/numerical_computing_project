import numpy as np
from typing import Dict, Any
from decimal import Decimal
from exceptions import ValidationError
from solvers.gauss_elimination_solver import GaussEliminationSolver
from solvers.gauss_jordan_elimination_solver import GaussJordanEliminationSolver
from solvers.lu_decomposition_solver import LUDecompositionSolver
from solvers.jacobi_iteration_solver import JacobiIterationSolver
from solvers.gauss_seidel_iteration_solver import GaussSeidelIterationSolver
from solvers.Bisection_solver import BisectionSolver
from solvers.False_Position_solver import FalsePositionSolver
import math

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

        elif method == "bisection":
   
            func_expr = parameters.get("function")
            xl = parameters.get("xl")
            xu = parameters.get("xu")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)
            
            if func_expr is None or xl is None or xu is None:
                raise ValidationError(
                    "Bisection method requires function xl and xu parameters"
                )
            
         
            try:
      
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))
            except (ValueError, TypeError) as e:
                raise ValidationError(f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}")
            
       
            def func(x: Decimal) -> Decimal:
                try:
          
                    import math
                    namespace = {
                        'x': x,
                        'Decimal': Decimal,
                        'abs': abs,
                        'sin': lambda val: Decimal(str(math.sin(float(val)))),
                        'cos': lambda val: Decimal(str(math.cos(float(val)))),
                        'tan': lambda val: Decimal(str(math.tan(float(val)))),
                        'exp': lambda val: Decimal(str(math.exp(float(val)))),
                        'log': lambda val: Decimal(str(math.log(float(val)))),
                        'sqrt': lambda val: Decimal(str(math.sqrt(float(val)))),
                    }
                    result = eval(func_expr, {"__builtins__": {}}, namespace)
                    if  not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result
                
                except Exception as e:
                    raise ValidationError(f"Error evaluating function '{func_expr}': {str(e)}")
            
            return BisectionSolver(
                xl=xl_decimal,
                xu=xu_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        
        elif method == "false-position":

            func_expr = parameters.get("function")
            xl = parameters.get("xl")
            xu = parameters.get("xu")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)
            
            if func_expr is None or xl is None or xu is None:
                raise ValidationError(
                    "flase-position method requires function xl and xu parameters"
                )
          
            try:
             
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))

            except (ValueError, TypeError) as e:
                raise ValidationError(f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}")
            
            def func(x: Decimal) -> Decimal:
                try:

                    namespace = {
                        'x': x,
                        'Decimal': Decimal,
                        'abs': abs,
                        'sin': lambda val: Decimal(str(math.sin(float(val)))),
                        'cos': lambda val: Decimal(str(math.cos(float(val)))),
                        'tan': lambda val: Decimal(str(math.tan(float(val)))),
                        'exp': lambda val: Decimal(str(math.exp(float(val)))),
                        'log': lambda val: Decimal(str(math.log(float(val)))),
                        'sqrt': lambda val: Decimal(str(math.sqrt(float(val)))),
                    }
                    result = eval(func_expr, {"__builtins__": {}}, namespace)
                    if not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result
                except Exception as e:
                    raise ValidationError(f"Error evaluating function '{func_expr}': {str(e)}")
            
            return FalsePositionSolver(
                xl=xl_decimal,
                xu=xu_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        else:
            raise ValidationError(f"Unknown method: {method}")
            
