from typing import List, Optional

from .base import Generator
from ..exceptions import GeneratorValidationError


class LCGenerator(Generator):
    """Generador Congruencial Lineal (LCG): X_{i+1} = (a * X_i + c) mod m."""

    def __init__(self, semilla: int, a: int, c: int, m: int):
        self.semilla = semilla
        self.a = a
        self.c = c
        self.m = m
        self.validate_parameters()

    def validate_parameters(self) -> None:
        if self.m <= 0:
            raise GeneratorValidationError("El módulo 'm' debe ser mayor que 0.")
        if not (0 <= self.semilla < self.m):
            raise GeneratorValidationError(
                f"La semilla {self.semilla} debe estar en el rango [0, {self.m - 1}]."
            )
        if not (0 <= self.a < self.m):
            raise GeneratorValidationError(
                f"El multiplicador 'a' ({self.a}) debe estar en el rango [0, {self.m - 1}]."
            )
        if not (0 <= self.c < self.m):
            raise GeneratorValidationError(
                f"El incremento 'c' ({self.c}) debe estar en el rango [0, {self.m - 1}]."
            )

    def generate(self, n: int) -> List[float]:
        if n < 0:
            raise GeneratorValidationError(
                "La cantidad 'n' debe ser un entero no negativo."
            )

        results = []
        x = self.semilla
        for _ in range(n):
            x = (self.a * x + self.c) % self.m
            results.append(x / (self.m - 1))
        return results


class MCGenerator(Generator):
    """Generador Congruencial Multiplicativo (MCG): X_{i+1} = (a * X_i) mod m."""

    def __init__(self, semilla: int, a: int, m: int):
        self.semilla = semilla
        self.a = a
        self.m = m
        self.validate_parameters()

    def validate_parameters(self) -> None:
        if self.m <= 0:
            raise GeneratorValidationError("El módulo 'm' debe ser mayor que 0.")
        if not (0 < self.semilla < self.m):
            raise GeneratorValidationError(
                f"La semilla {self.semilla} debe estar en el rango [1, {self.m - 1}]."
            )
        if not (0 <= self.a < self.m):
            raise GeneratorValidationError(
                f"El multiplicador 'a' ({self.a}) debe estar en el rango [0, {self.m - 1}]."
            )

    def generate(self, n: int) -> List[float]:
        if n < 0:
            raise GeneratorValidationError(
                "La cantidad 'n' debe ser un entero no negativo."
            )

        results = []
        x = self.semilla
        for _ in range(n):
            x = (self.a * x) % self.m
            results.append(x / (self.m - 1))
        return results


class MidSquareGenerator(Generator):
    """Generador de Cuadrados Medios (Mid-Square): X_{i+1} = dígitos centrales de X_i²."""

    def __init__(self, semilla: int, digits: Optional[int] = None):
        self.semilla = semilla
        self.digits = digits
        self.validate_parameters()

    def validate_parameters(self) -> None:
        if self.semilla < 0:
            raise GeneratorValidationError(
                "La semilla debe ser un entero no negativo."
            )

        if self.digits is None:
            self.digits = len(str(self.semilla))

        if self.digits <= 0 or self.digits % 2 != 0:
            raise GeneratorValidationError(
                f"La cantidad de dígitos ({self.digits}) debe ser un entero positivo par."
            )

        max_value = 10 ** self.digits - 1
        if self.semilla > max_value:
            raise GeneratorValidationError(
                f"La semilla {self.semilla} excede el valor máximo para {self.digits} dígitos ({max_value})."
            )

    def generate(self, n: int) -> List[float]:
        if n < 0:
            raise GeneratorValidationError(
                "La cantidad 'n' debe ser un entero no negativo."
            )

        results = []
        x = self.semilla
        divisor = 10 ** self.digits

        for _ in range(n):
            squared_str = str(x ** 2)

            if len(squared_str) < self.digits:
                squared_str = squared_str.zfill(self.digits)

            if len(squared_str) % 2 != 0:
                squared_str = "0" + squared_str

            total_len = len(squared_str)
            start = (total_len - self.digits) // 2
            end = start + self.digits
            x = int(squared_str[start:end])
            results.append(x / divisor)

        return results
