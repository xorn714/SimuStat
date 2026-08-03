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


def validate_probability(p: float) -> None:
    """Valida que una probabilidad esté en [0, 1]."""
    if not 0 <= p <= 1:
        raise GeneratorValidationError(
            f"La probabilidad 'p' ({p}) debe estar en [0, 1]."
        )


def validate_positive_count(n: int) -> None:
    """Valida que un conteo sea un entero positivo."""
    if n <= 0:
        raise GeneratorValidationError(
            f"El conteo 'n' ({n}) debe ser mayor que 0."
        )
