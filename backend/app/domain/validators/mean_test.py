import numpy as np
from scipy.stats import norm
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class MeanTest:
    """Prueba de medias: valida que la media muestral sea igual a la media teórica."""

    def __init__(
        self,
        alpha: float = 0.05,
        expected_mean: float = 0.5,
        expected_variance: float = 1.0 / 12.0,
    ):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        if expected_variance <= 0:
            raise StatisticalTestError("La varianza teórica debe ser mayor que 0.")
        self.alpha = alpha
        self.expected_mean = expected_mean
        self.expected_variance = expected_variance
        self.z_critical = float(norm.ppf(1 - alpha / 2))

    def test(self, numbers: List[float]) -> Tuple[Tuple[float, float], float, bool]:
        """
        Realiza la prueba de medias.

        Returns:
            (límites (LI, LS), estadístico (media muestral), passed)
        """
        n = len(numbers)
        if n <= 0:
            raise StatisticalTestError(
                "El tamaño de la muestra debe ser mayor que 0."
            )

        sample_mean = float(np.mean(numbers))
        precision = self.z_critical * (self.expected_variance / n) ** 0.5

        lower_limit = self.expected_mean - precision
        upper_limit = self.expected_mean + precision
        passed = lower_limit <= sample_mean <= upper_limit

        return (lower_limit, upper_limit), sample_mean, passed
