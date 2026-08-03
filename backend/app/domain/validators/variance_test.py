import numpy as np
from scipy.stats import chi2
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class VarianceTest:
    """Prueba de varianza: valida que la varianza muestral sea igual a la varianza teórica."""

    def __init__(self, alpha: float = 0.05, expected_variance: float = 1.0 / 12.0):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        if expected_variance <= 0:
            raise StatisticalTestError("La varianza teórica debe ser mayor que 0.")
        self.alpha = alpha
        self.expected_variance = expected_variance

    def test(self, numbers: List[float]) -> Tuple[Tuple[float, float], float, bool]:
        """
        Realiza la prueba de varianza.

        Returns:
            (límites (LI, LS), estadístico (varianza muestral), passed)
        """
        n = len(numbers)
        if n <= 1:
            raise StatisticalTestError(
                "El tamaño de la muestra debe ser mayor que 1 para calcular la varianza."
            )

        sample_var = float(np.var(numbers, ddof=1))

        df = n - 1
        chi_lower = float(chi2.ppf(self.alpha / 2, df=df))
        chi_upper = float(chi2.ppf(1 - self.alpha / 2, df=df))

        lower_limit = self.expected_variance * chi_lower / df
        upper_limit = self.expected_variance * chi_upper / df
        passed = lower_limit <= sample_var <= upper_limit

        return (lower_limit, upper_limit), sample_var, passed
