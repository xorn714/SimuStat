import numpy as np
from scipy.stats import kstwo
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class KSTest:
    """Prueba de bondad de ajuste de Kolmogorov-Smirnov para U(0,1)."""

    def __init__(self, alpha: float = 0.05):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        self.alpha = alpha

    def test(self, numbers: List[float]) -> Tuple[Tuple[float, float], float, bool]:
        """
        Realiza la prueba KS.

        Returns:
            (límites (0.0, D_critical), estadístico D, passed)
        """
        n = len(numbers)
        if n <= 0:
            raise StatisticalTestError(
                "El tamaño de la muestra debe ser mayor que 0."
            )

        sorted_numbers = np.sort(numbers)
        i = np.arange(1, n + 1)

        d_plus = np.max(i / n - sorted_numbers)
        d_minus = np.max(sorted_numbers - (i - 1) / n)
        d_statistic = float(max(d_plus, d_minus))

        d_critical = float(kstwo.ppf(1 - self.alpha, n))
        passed = d_statistic < d_critical

        return (0.0, d_critical), d_statistic, passed
