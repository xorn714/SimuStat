from scipy.stats import norm
from typing import List, Tuple

from ..exceptions import StatisticalTestError


class RunsTest:
    """Prueba de rachas (runs test) arriba y abajo de la media 0.5."""

    def __init__(self, alpha: float = 0.05):
        if not 0 < alpha < 1:
            raise StatisticalTestError("alpha debe estar en (0, 1).")
        self.alpha = alpha
        self.z_critical = float(norm.ppf(1 - alpha / 2))

    def test(self, numbers: List[float]) -> Tuple[Tuple[float, float], float, bool]:
        """
        Realiza la prueba de rachas.

        Returns:
            (límites (LI, LS), estadístico Z_0, passed)
        """
        n = len(numbers)
        if n <= 1:
            raise StatisticalTestError(
                "El tamaño de la muestra debe ser mayor que 1 para la prueba de rachas."
            )

        signs = [1 if x >= 0.5 else 0 for x in numbers]
        n1 = sum(signs)
        n2 = n - n1

        runs = 1
        for i in range(1, n):
            if signs[i] != signs[i - 1]:
                runs += 1

        lower_limit = -self.z_critical
        upper_limit = self.z_critical

        if n1 == 0 or n2 == 0:
            return (lower_limit, upper_limit), float("inf"), False

        mu_runs = (2 * n1 * n2) / n + 1.0

        var_numerator = 2 * n1 * n2 * (2 * n1 * n2 - n)
        var_denominator = (n ** 2) * (n - 1)

        if var_denominator == 0 or var_numerator <= 0:
            z_statistic = 0.0
        else:
            sigma_runs = (var_numerator / var_denominator) ** 0.5
            z_statistic = (runs - mu_runs) / sigma_runs

        passed = lower_limit <= z_statistic <= upper_limit
        return (lower_limit, upper_limit), float(z_statistic), passed
