from abc import ABC, abstractmethod
from typing import Any, Dict


# base class for a step in the solution process
class Step(ABC):
    step_type: str

    def __init__(self, step_type: str):
        self.step_type = step_type

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
