from decimal import Decimal
import numpy as np
from typing import List, Tuple, Optional
from exceptions import ValidationError
from sympy import sympify
from sympy.core.sympify import SympifyError
import re

class LinearSystemValidator:
    @staticmethod
    def validate_system(
        A: List[List[Decimal]], b: List[Decimal]
    ) -> Tuple[np.ndarray, np.ndarray]:
        try:
            A_matrix = np.array(A, dtype=Decimal)
            b_vector = np.array(b, dtype=Decimal)
        except (ValueError, TypeError) as e:
            raise ValidationError(
                f"Coefficients must be numbers:{str(e)}"
            )  # that's the one will need to change later on for the bonus

        if A_matrix.ndim != 2:
            raise ValidationError("Coefficient matrix must be 2-dimensional.")

        if b_vector.ndim != 1:
            raise ValidationError("Constants vector must be 1-dimensional.")

        n_equations, n_variables = A_matrix.shape

        if n_equations != n_variables:
            raise ValidationError(
                f"Number of equations ({n_equations}) must equal number of variables ({n_variables})."
            )

        return A_matrix, b_vector

    @staticmethod
    def validate_precision(precision: Optional[int]) -> int:
        if precision is None:
            return 10  # a7la defalut

        try:
            prec = int(precision)
            if prec < 1:
                raise ValidationError("Precision must be more than 1")
            return prec
        except (ValueError, TypeError):
            raise ValidationError("Precision  must be an integer")
        
class FunctionValidator:
    @staticmethod
    def validate_and_parse(equation_str: str):
        """Validates and parses a mathematical equation string into a SymPy expression.
        """

        # if the equation string is empty or None, raise an error
        if not equation_str or not equation_str.strip():
            raise ValidationError("Equation cannot be empty.")
        

        # preprocess the equation string to replace common mathematical notations
        # e.g., replace '^' with '**' for exponentiation
        # and replace 'e' with 'E' for scientific notation 
        # to make it compatible with SymPy syntax also be sure that if the user is writing sec(x) or cosec(x) the function will not covert the e to E
        try:
            equation_str = equation_str.replace("^", "**")
            equation_str = re.sub(r'\be\b', 'E', equation_str)
        except Exception as e:
            raise ValidationError(f"Error in preprocessing the equation: {str(e)}")
        
        # try to parse the equation string into a SymPy expression

        try:
            expr = sympify(equation_str)
        except (SympifyError, SyntaxError):
            raise ValidationError("Invalid equation format. Please check your syntax.")

        # check if the number of free symbols in the expression is only 1 or not
        free_symbols = expr.free_symbols
        
        if len(free_symbols) != 1:
            raise ValidationError(f"Equation must contain only one variable. Found: {free_symbols}")
        
        # check if the variable is 'x' or not
        variable = list(free_symbols)[0]
        if variable.name != 'x':
            raise ValidationError(f"Variable must be 'x'. Found: '{variable.name}'")
        
        # All validations passed, return the parsed expression
        # The return type is sympy expression
        return expr