import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple, Union
from solution_result import SolutionResult

class LinearSystemSolver(ABC):
    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int = 6):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision

    @abstractmethod
    def solve(self) -> SolutionResult:
        pass

    def round_to_sf(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        def round_single(num):
            if num == 0:
                return 0
            try:
                order= np.floor(np.log10(abs(num)))
                scale =10**(self.precision - 1 - order)
                result= round(num * scale) / scale
                return result
            except (ValueError,OverflowError):
                return num
        if isinstance(x, np.ndarray):
            return np.vectorize(round_single)(x)
        else:
            return round_single(x)
    def round_solution(self, x: np.ndarray) -> np.ndarray:
        return self.round_to_sf(x)

    def safe_divide(self,numerator:float, denominator: float) -> float:
        if abs(denominator) <1e-12:
            raise ZeroDivisionError("divison by zero encountered bad thing")
        return self.round_to_sf(numerator/denominator)

    def safe_multiply(self, a:float,b:float) -> float:

        return self.round_to_sf(a*b)

    def safe_subtract(self,a:float,b:float) -> float:

        return self.round_to_sf(a-b)

    def safe_add(self,a:float,b:float) -> float:
        return self.round_to_sf(a+b)
    def dot_product_with_rounding(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
 
        if len(vec1)!=len(vec2):
            raise ValueError("vectors must have same length sorry")
        result = 0.0
        for i in range(len(vec1)):
            product= self.safe_multiply(vec1[i],vec2[i])
            result =self.safe_add(result,product)
        return result

    def update_matrix_row(self,target_row:np.ndarray,source_row:np.ndarray,factor:float) -> np.ndarray:
        updated_row =target_row.copy()
        for j in range(len(target_row)):
            elimination_term = self.safe_multiply(factor,source_row[j])
            updated_row[j] =self.safe_subtract(target_row[j],elimination_term)
        return updated_row
    def update_vector_element(self,target:float,source:float,factor:float) -> float:
        elimination_term = self.safe_multiply(factor,source)
        return self.safe_subtract(target,elimination_term)

    @staticmethod
    def partial_pivot(A: np.ndarray, b: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        n = len(b)
        max_idx = k + np.argmax(np.abs(A[k:, k]))
        if max_idx != k:
            A[[k, max_idx]] = A[[max_idx, k]]
            b[[k, max_idx]] = b[[max_idx, k]]
        return A, b