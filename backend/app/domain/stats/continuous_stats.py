import math
from typing import Any, Dict, List, Tuple

from ..exceptions import StatsCalculationError


class ContinuousStatsCalculator:
    """Calcula estadísticos empíricos y teóricos e histograma para distribuciones continuas."""

    @staticmethod
    def calculate_stats(
        values: List[float],
        dist_name: str,
        dist_params: Dict[str, float],
    ) -> Tuple[Dict[str, float], Dict[str, Any]]:
        """
        Calcula los estadísticos empíricos vs teóricos e histograma de frecuencias
        con la curva teórica de densidad de probabilidad.

        Returns:
            (stats_dict, histogram_dict)
        """
        n = len(values)
        if n == 0:
            raise StatsCalculationError("La lista de valores está vacía.")

        emp_mean = sum(values) / n
        emp_var = sum((x - emp_mean) ** 2 for x in values) / (n - 1) if n > 1 else 0.0

        theo_mean = 0.0
        theo_var = 0.0
        pdf_func = lambda x: 0.0

        dist = dist_name.lower()

        if dist == "uniform":
            a = dist_params.get("a", 0.0)
            b = dist_params.get("b", 1.0)
            theo_mean = (a + b) / 2.0
            theo_var = ((b - a) ** 2) / 12.0
            pdf_func = lambda x: (1.0 / (b - a)) if a <= x <= b else 0.0

        elif dist == "exponential":
            lambd = dist_params.get("lambd", 1.0)
            theo_mean = 1.0 / lambd
            theo_var = 1.0 / (lambd ** 2)
            pdf_func = lambda x: (lambd * math.exp(-lambd * x)) if x >= 0 else 0.0

        elif dist == "normal":
            mean = dist_params.get("mean", 0.0)
            std_dev = dist_params.get("std_dev", 1.0)
            theo_mean = mean
            theo_var = std_dev ** 2
            pdf_func = lambda x: (
                (1.0 / (std_dev * math.sqrt(2.0 * math.pi)))
                * math.exp(-0.5 * (((x - mean) / std_dev) ** 2))
            )

        elif dist == "weibull":
            alpha = dist_params.get("alpha", 1.0)
            beta = dist_params.get("beta", 1.0)
            gamma1 = math.gamma(1.0 + 1.0 / beta)
            gamma2 = math.gamma(1.0 + 2.0 / beta)
            theo_mean = alpha * gamma1
            theo_var = (alpha ** 2) * (gamma2 - (gamma1 ** 2))
            pdf_func = lambda x: (
                (beta / alpha)
                * ((x / alpha) ** (beta - 1.0))
                * math.exp(-((x / alpha) ** beta))
                if x > 0
                else 0.0
            )

        stats = {
            "empirical_mean": round(emp_mean, 4),
            "theoretical_mean": round(theo_mean, 4),
            "mean_diff": round(abs(emp_mean - theo_mean), 4),
            "empirical_variance": round(emp_var, 4),
            "theoretical_variance": round(theo_var, 4),
            "variance_diff": round(abs(emp_var - theo_var), 4),
            "min": round(min(values), 4),
            "max": round(max(values), 4),
        }

        k = int(math.ceil(1.0 + 3.322 * math.log10(n)))
        k = max(5, min(k, 25))

        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val
        if range_val == 0:
            range_val = 1.0

        width = range_val / k
        bin_counts = [0] * k

        for val in values:
            idx = int((val - min_val) / width)
            if idx >= k:
                idx = k - 1
            bin_counts[idx] += 1

        bins_data = []
        for i in range(k):
            bin_start = min_val + i * width
            bin_end = bin_start + width
            bin_mid = (bin_start + bin_end) / 2.0
            count = bin_counts[i]
            emp_density = count / (n * width)
            theo_density = pdf_func(bin_mid)

            bins_data.append({
                "bin": f"[{round(bin_start, 2)}, {round(bin_end, 2)})",
                "bin_start": round(bin_start, 3),
                "bin_end": round(bin_end, 3),
                "mid": round(bin_mid, 3),
                "count": count,
                "empirical_density": round(emp_density, 4),
                "theoretical_density": round(theo_density, 4),
            })

        histogram = {
            "bins": bins_data,
            "bin_width": round(width, 4),
            "total_count": n,
        }

        return stats, histogram
