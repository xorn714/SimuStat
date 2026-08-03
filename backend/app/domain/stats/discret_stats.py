import math
from typing import List, Dict, Any
from collections import Counter
from ..exceptions import StatsCalculationError

class DiscreteStatsCalculator:
    """
    Calcula estadísticos para distribuciones discretas.
    """

    @staticmethod
    def _cdf_from_pmf(pmf, start: int, end=None):
        """Construye una CDF discreta F(x) sumando la pmf sobre el soporte."""
        def cdf(x):
            if x < start:
                return 0.0
            limit = min(int(x), end) if end is not None else int(x)
            total = 0.0
            for k in range(start, limit + 1):
                total += pmf(k)
            return min(total, 1.0)
        return cdf

    @staticmethod
    def get_pmf(dist_name: str, dist_params: Dict[str, float]):
        """Devuelve la función de masa de probabilidad teórica P(X = k) de una distribución discreta."""
        dist = dist_name.lower()

        if dist == "bernoulli":
            p = dist_params.get('p', 0.5)
            def bernoulli_pmf(k):
                if k == 0:
                    return 1.0 - p
                if k == 1:
                    return p
                return 0.0
            return bernoulli_pmf

        elif dist == "binomial":
            n = int(dist_params.get('n', 10))
            p = dist_params.get('p', 0.5)
            return lambda k: (
                math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))
                if 0 <= k <= n else 0.0
            )

        elif dist == "poisson":
            lambd = dist_params.get('lambda', 1.0)
            return lambda k: (
                math.exp(-lambd) * (lambd ** k) / math.factorial(k)
                if k >= 0 else 0.0
            )

        elif dist == "geometric":
            p = dist_params.get('p', 0.5)
            return lambda k: ((1.0 - p) ** (k - 1)) * p if k >= 1 else 0.0

        elif dist == "negative_binomial":
            r = int(dist_params.get('r', 5))
            p = dist_params.get('p', 0.5)
            return lambda k: (
                math.comb(k - 1, r - 1) * (p ** r) * ((1.0 - p) ** (k - r))
                if k >= r else 0.0
            )

        elif dist == "hypergeometric":
            N = int(dist_params.get('N', 100))
            K = int(dist_params.get('K', 50))
            n = int(dist_params.get('n', dist_params.get('n_sample', 10)))
            lo = max(0, n - (N - K))
            hi = min(n, K)
            denom = math.comb(N, n)
            return lambda k: (
                (math.comb(K, k) * math.comb(N - K, n - k)) / denom
                if lo <= k <= hi else 0.0
            )

        raise StatsCalculationError(
            f"Distribución discreta no soportada para PMF: '{dist_name}'."
        )

    @staticmethod
    def get_cdf(dist_name: str, dist_params: Dict[str, float]):
        """Devuelve la función de distribución acumulada teórica F(x) de una distribución discreta."""
        dist = dist_name.lower()
        pmf = DiscreteStatsCalculator.get_pmf(dist_name, dist_params)

        if dist == "bernoulli":
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, 0, end=1)
        elif dist == "binomial":
            n = int(dist_params.get('n', 10))
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, 0, end=n)
        elif dist == "poisson":
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, 0)
        elif dist == "geometric":
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, 1)
        elif dist == "negative_binomial":
            r = int(dist_params.get('r', 5))
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, r)
        elif dist == "hypergeometric":
            N = int(dist_params.get('N', 100))
            K = int(dist_params.get('K', 50))
            n = int(dist_params.get('n', dist_params.get('n_sample', 10)))
            lo = max(0, n - (N - K))
            hi = min(n, K)
            return DiscreteStatsCalculator._cdf_from_pmf(pmf, lo, end=hi)

        raise StatsCalculationError(
            f"Distribución discreta no soportada para CDF: '{dist_name}'."
        )

    @staticmethod
    def calculate_stats(
        values: List[int],
        dist_name: str,
        dist_params: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calcula estadísticos empíricos vs teóricos para distribuciones discretas.
        
        Args:
            values: Lista de valores generados
            dist_name: Tipo de distribución ('bernoulli', 'binomial', 'poisson', 
                      'geometric', 'negative_binomial', 'hypergeometric')
            dist_params: Parámetros de la distribución
        
        Returns:
            Diccionario con estadísticos
        """
        n = len(values)
        if n == 0:
            raise StatsCalculationError("La lista de valores está vacía.")
        
        # Estadísticos empíricos
        empirical_mean = sum(values) / n
        empirical_variance = sum((x - empirical_mean) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
        
        # Frecuencias
        freq_counter = Counter(values)
        frequencies = dict(sorted(freq_counter.items()))
        relative_frequencies = {
            k: v / n for k, v in frequencies.items()
        }
        
        # Estadísticos teóricos según la distribución
        theoretical_stats = DiscreteStatsCalculator._calculate_theoretical_stats(
            dist_name, dist_params
        )
        
        return {
            "sample_size": n,
            "empirical_mean": round(empirical_mean, 6),
            "empirical_variance": round(empirical_variance, 6),
            "theoretical_mean": round(theoretical_stats["mean"], 6),
            "theoretical_variance": round(theoretical_stats["variance"], 6),
            "mean_diff": round(abs(empirical_mean - theoretical_stats["mean"]), 6),
            "variance_diff": round(abs(empirical_variance - theoretical_stats["variance"]), 6),
            "frequencies": frequencies,
            "relative_frequencies": relative_frequencies,
            "unique_values": len(frequencies),
            "min_value": min(values),
            "max_value": max(values),
            "mode": max(frequencies.items(), key=lambda x: x[1])[0] if frequencies else None,
        }
    
    @staticmethod
    def _calculate_theoretical_stats(
        dist_name: str,
        params: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calcula la media y varianza teóricas para una distribución discreta.
        """
        dist_name = dist_name.lower()
        
        if dist_name == "bernoulli":
            p = params.get('p', 0.5)
            mean = p
            variance = p * (1 - p)
            
        elif dist_name == "binomial":
            n = params.get('n', 10)
            p = params.get('p', 0.5)
            mean = n * p
            variance = n * p * (1 - p)
            
        elif dist_name == "poisson":
            lambd = params.get('lambda', 1.0)
            mean = lambd
            variance = lambd
            
        elif dist_name == "geometric":
            p = params.get('p', 0.5)
            mean = 1.0 / p
            variance = (1.0 - p) / (p * p)
            
        elif dist_name == "negative_binomial":
            r = params.get('r', 5)
            p = params.get('p', 0.5)
            mean = r / p
            variance = r * (1.0 - p) / (p * p)
            
        elif dist_name == "hypergeometric":
            N = params.get('N', 100)
            K = params.get('K', 50)
            n = params.get('n', params.get('n_sample', 10))
            mean = n * (K / N)
            variance = n * (K / N) * (1 - K / N) * ((N - n) / (N - 1))
            
        else:
            mean = 0.0
            variance = 0.0
        
        return {"mean": mean, "variance": variance}
    
    @staticmethod
    def create_histogram_data(
        values: List[int],
        frequencies: Dict[int, int]
    ) -> List[Dict[str, Any]]:
        """
        Crea datos para un histograma de barras de la distribución discreta.
        """
        n = len(values)
        if n == 0:
            return []
        
        data = []
        for value, count in frequencies.items():
            data.append({
                "value": value,
                "count": count,
                "relative_frequency": count / n,
                "cumulative_count": 0,  # Se calculará después
                "cumulative_relative": 0  # Se calculará después
            })
        
        # Calcular acumulados
        cumulative_count = 0
        cumulative_relative = 0.0
        for item in data:
            cumulative_count += item["count"]
            cumulative_relative += item["relative_frequency"]
            item["cumulative_count"] = cumulative_count
            item["cumulative_relative"] = round(cumulative_relative, 4)
        
        return data