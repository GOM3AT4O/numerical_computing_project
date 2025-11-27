from decimal import Decimal
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple
from row_operation import RowOperation
from step import Step
from solution_result import SolutionResult


class LinearSystemSolver(ABC):
    A: np.ndarray
    b: np.ndarray
    n: int
    precision: int
    steps: List[Step]

    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int = 6):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision
        self.steps = []

    @abstractmethod
    def solve(self) -> SolutionResult:
        pass

    def safe_divide(self, numerator: Decimal, denominator: Decimal) -> Decimal:
        if abs(denominator) < 1e-12:
            raise ZeroDivisionError("Divison by zero encountered")
        return numerator / denominator

    def update_matrix_row(
        self, target_row: np.ndarray, source_row: np.ndarray, factor: Decimal
    ) -> np.ndarray:
        updated_row = target_row.copy()
        for j in range(len(target_row)):
            elimination_term = factor * source_row[j]
            updated_row[j] = target_row[j] - elimination_term
        return updated_row

    def update_vector_element(
        self, target: Decimal, source: Decimal, factor: Decimal
    ) -> Decimal:
        elimination_term = factor * source
        return target - elimination_term

    def partial_pivot(
        self, A: np.ndarray, b: np.ndarray, k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        max_idx = k + np.argmax(np.abs(A[k:, k]))
        if max_idx != k:
            old_matrix = np.column_stack([A, b])
            A[[k, max_idx]] = A[[max_idx, k]]
            b[[k, max_idx]] = b[[max_idx, k]]
            new_matrix = np.column_stack([A, b])
            step = RowOperation.swap(old_matrix, new_matrix, k, int(max_idx))
            self.steps.append(step)
        return A, b
    
    # for calculating the scaling values of each row in the coefficient matrix A    
    @staticmethod
    def Calculating_Scaling_values(A: np.ndarray) -> np.ndarray:
        n = A.shape[0] # number of rows in A
        s = np.full(n, Decimal(0)) # initialize scaling factors array
        for i in range(n): # iterate through each row
            s[i] = np.max(np.abs(A[i, :])) # find the maximum absolute value in the row
        return s # return the array of scaling factors
       
    # for finding the pivot of each row based on the scaling values in a specific column k
    @staticmethod
    def find_pivot_row(A: np.ndarray, s: np.ndarray, k: int) -> int:
        n = A.shape[0] # number of rows in A
        ratios = np.abs(A[k:, k]) / s[k:] # calculate the ratio of the absolute value of the pivot element to the scaling factor for each row
        pivot_index = k + np.argmax(ratios) # find the index of the maximum ratio
        return pivot_index # return the index of the pivot row
    
    @staticmethod
    def Scaling_Partial_Pivot(A: np.ndarray, b: np.ndarray, s: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        n = len(b)
        max_idx = LinearSystemSolver.find_pivot_row(A, s, k) # find the pivot row using scaling
        # if the pivot row is not the current row, swap them
        if max_idx != k:
            A[[k, max_idx]] = A[[max_idx, k]]
            b[[k, max_idx]] = b[[max_idx, k]]
            s[[k, max_idx]] = s[[max_idx, k]]  # 25adet baly 2ny 2badel 2l scaling values kman
        # returning the updated A and b
        return A, b