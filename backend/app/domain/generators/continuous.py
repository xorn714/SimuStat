import math
from typing import List
from .base import validate_uniform_sequence, validate_positive_lambda
from ..exceptions import GeneratorValidationError

class ContinuousDistributionGenerator:
    """Generador de variables aleatorias continuas."""
    
    @staticmethod
    def uniform(u_list: List[float], a: float, b: float) -> List[float]:
        """Genera Uniforme Continua U(a, b)."""
        if a >= b:
            raise GeneratorValidationError(
                f"El límite inferior 'a' ({a}) debe ser menor que 'b' ({b})."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1].")
        return [a + (b - a) * u for u in u_list]
    
    @staticmethod
    def exponential(u_list: List[float], beta: float) -> List[float]:
        """Genera Exponencial con media beta (tiempo promedio)."""
        validate_positive_lambda(beta)
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1].")
        
        results = []
        for u in u_list:
            u_safe = max(min(u, 1.0 - 1e-12), 1e-12)
            val = -beta * math.log(1.0 - u_safe)
            results.append(val)
        return results
    
    @staticmethod
    def normal(u_list: List[float], mean: float, std_dev: float) -> List[float]:
        """Genera Normal N(mean, std_dev²) usando Box-Muller."""
        if std_dev <= 0:
            raise GeneratorValidationError(
                f"La desviación estándar ({std_dev}) debe ser mayor que 0."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1].")
        
        results = []
        n = len(u_list)
        for i in range(0, n, 2):
            u1 = max(u_list[i], 1e-12)
            u2 = u_list[i + 1] if (i + 1 < n) else u_list[0]
            
            z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
            
            results.append(mean + z0 * std_dev)
            if i + 1 < n:
                results.append(mean + z1 * std_dev)
        
        return results[:n]
    
    @staticmethod
    def weibull(u_list: List[float], alpha: float, beta: float) -> List[float]:
        """Genera Weibull(alpha, beta)."""
        if alpha <= 0:
            raise GeneratorValidationError(
                f"El parámetro de escala alpha ({alpha}) debe ser mayor que 0."
            )
        if beta <= 0:
            raise GeneratorValidationError(
                f"El parámetro de forma beta ({beta}) debe ser mayor que 0."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1].")
        
        results = []
        for u in u_list:
            u_safe = max(min(u, 1.0 - 1e-12), 1e-12)
            val = alpha * ((-math.log(1.0 - u_safe)) ** (1.0 / beta))
            results.append(val)
        return results