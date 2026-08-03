from abc import ABC, abstractmethod
from typing import List

from ..exceptions import GeneratorValidationError


class Generator(ABC):
    """Clase base abstracta para generadores de números pseudoaleatorios."""

    @abstractmethod
    def generate(self, n: int) -> List[float]:
        """Genera una secuencia de n números en [0, 1)."""
        pass

    @abstractmethod
    def validate_parameters(self) -> None:
        """Valida los parámetros del generador."""
        pass


def validate_uniform_sequence(sequence: List[float]) -> bool:
    """Valida que una secuencia esté en [0, 1]."""
    return all(0 <= x <= 1 for x in sequence)


def validate_positive_lambda(lambd: float) -> None:
    """Valida que lambda sea positivo."""
    if lambd <= 0:
        raise GeneratorValidationError(
            f"El parámetro lambda '{lambd}' debe ser mayor que 0."
        )
