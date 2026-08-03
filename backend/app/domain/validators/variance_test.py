import numpy as np
from scipy.stats import chi2
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class VarianceTest:
    """Prueba de varianza para U(0,1): valida que la varianza muestral sea 1/12."""

    def __init__(self, alpha: float = 0.05):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        self.alpha = alpha

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

        lower_limit = chi_lower / (12 * df)
        upper_limit = chi_upper / (12 * df)
        passed = lower_limit <= sample_var <= upper_limit

        return (lower_limit, upper_limit), sample_var, passed
