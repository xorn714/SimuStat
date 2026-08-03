import numpy as np
from scipy.stats import norm
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class MeanTest:
    """Prueba de medias para U(0,1): valida que la media muestral sea 0.5."""

    def __init__(self, alpha: float = 0.05):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        self.alpha = alpha
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
        precision = self.z_critical * (1.0 / (12 * n) ** 0.5)

        lower_limit = 0.5 - precision
        upper_limit = 0.5 + precision
        passed = lower_limit <= sample_mean <= upper_limit

        return (lower_limit, upper_limit), sample_mean, passed
