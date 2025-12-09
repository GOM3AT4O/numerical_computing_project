import numpy as np
from typing import Dict, Any
from decimal import Decimal
import re
import math

def preprocess_function_expression(func_expr: str) -> str:
    """
    Convert numeric literals in the expression to Decimal format.
    E.g., '0.5' becomes 'Decimal("0.5")', '2' becomes 'Decimal("2")'
    """
    # Pattern to match numbers (integer or decimal) that are not already in Decimal() or part of a word
    # This regex matches: integers, decimals, and scientific notation
    pattern = r'\b(\d+\.?\d*(?:[eE][+-]?\d+)?)\b'
    
    def replace_number(match):
        num = match.group(1)
        # Don't wrap if already inside Decimal()
        return f'Decimal("{num}")'
    
    # Replace all numeric literals with Decimal equivalents
    processed = re.sub(pattern, replace_number, func_expr)
    return processed


def create_function_from_expression(func_expr: str):
    """
    Create a function that evaluates the expression with Decimal precision.
    """
    # Preprocess the expression to convert literals to Decimal
    processed_expr = preprocess_function_expression(func_expr)
    
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
                'pow': lambda base, exp: Decimal(str(math.pow(float(base), float(exp)))),
                'pi': Decimal(str(math.pi)),
                'e': Decimal(str(math.e)),
            }
            result = eval(processed_expr, {"__builtins__": {}}, namespace)
            if not isinstance(result, Decimal):
                result = Decimal(str(result))
            return result
        except Exception as e:
            from exceptions import ValidationError
            raise ValidationError(f"Error evaluating function '{func_expr}': {str(e)}")
    
    return func


# UPDATED SOLVERFACTORY - Replace the bisection and false-position sections

class SolverFactory:
    @staticmethod
    def create_solver(
        method: str,
        A: np.ndarray,
        b: np.ndarray,
        precision: int,
        parameters: Dict[str, Any],
    ):
        # ... [keep your existing gauss-elimination, gauss-jordan-elimination, 
        #      lu-decomposition, jacobi-iteration, gauss-seidel-iteration methods] ...

        if method == "bisection":
            func_expr = parameters.get("function")
            xl = parameters.get("xl")
            xu = parameters.get("xu")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)
            
            if func_expr is None or xl is None or xu is None:
                from exceptions import ValidationError
                raise ValidationError(
                    "Bisection method requires function xl and xu parameters"
                )
            
            try:
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))
            except (ValueError, TypeError) as e:
                from exceptions import ValidationError
                raise ValidationError(f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}")
            
            # Use the helper function instead of inline eval
            func = create_function_from_expression(func_expr)
            
            from solvers.Bisection_solver import BisectionSolver
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
                from exceptions import ValidationError
                raise ValidationError(
                    "false-position method requires function xl and xu parameters"
                )
          
            try:
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))
            except (ValueError, TypeError) as e:
                from exceptions import ValidationError
                raise ValidationError(f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}")
            
            # Use the helper function instead of inline eval
            func = create_function_from_expression(func_expr)
            
            from solvers.False_Position_solver import FalsePositionSolver
            return FalsePositionSolver(
                xl=xl_decimal,
                xu=xu_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        
        else:
            from exceptions import ValidationError
            raise ValidationError(f"Unknown method: {method}")
        



        