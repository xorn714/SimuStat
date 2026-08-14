import math
from typing import List
from .base import validate_uniform_sequence, validate_probability
from ..exceptions import GeneratorValidationError

class DiscreteDistributionGenerator:
    """
    Generador de variables aleatorias discretas usando el método de transformada inversa.
    """
    
    @staticmethod
    def bernoulli(u_list: List[float], p: float) -> List[int]:
        """
        Genera una muestra de Bernoulli(p).
        
        Args:
            u_list: Lista de números U(0,1)
            p: Probabilidad de éxito (0 <= p <= 1)
        
        Returns:
            Lista de valores 0 o 1
        
        Fórmula: X = 1 si U < p, 0 en caso contrario
        """
        validate_probability(p)
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        return [1 if u < p else 0 for u in u_list]
    
    @staticmethod
    def binomial(u_list: List[float], n: int, p: float) -> List[int]:
        """
        Genera una muestra de Binomial(n, p).
        
        Args:
            u_list: Lista de números U(0,1)
            n: Número de ensayos
            p: Probabilidad de éxito (0 <= p <= 1)
        
        Returns:
            Lista de valores entre 0 y n
        
        Método: Suma de n variables Bernoulli independientes
        """
        if n <= 0:
            raise GeneratorValidationError(f"El número de ensayos 'n' ({n}) debe ser mayor que 0.")
        validate_probability(p)
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        results = []
        # Tomamos bloques de n números para cada observación
        for i in range(0, len(u_list), n):
            batch = u_list[i:i+n]
            if len(batch) < n:
                break  # Ignoramos el último bloque incompleto
            successes = sum(1 for u in batch if u < p)
            results.append(successes)
        
        return results
    
    @staticmethod
    def poisson(u_list: List[float], lambd: float) -> List[int]:
        """
        Genera una muestra de Poisson(lambda).
        
        Args:
            u_list: Lista de números U(0,1)
            lambd: Parámetro lambda (media) > 0
        
        Returns:
            Lista de valores enteros >= 0
        
        Método: Transformada inversa usando relación recursiva
        P(X = k) = P(X = k-1) * (lambda / k)
        """
        if lambd <= 0:
            raise GeneratorValidationError(f"El parámetro lambda ({lambd}) debe ser mayor que 0.")
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        results = []
        for u in u_list:
            x = 0
            # P(X = 0) = e^(-lambda)
            p_x = math.exp(-lambd)
            cumulative = p_x
            
            while u > cumulative:
                x += 1
                # Actualizar usando relación recursiva
                p_x = p_x * (lambd / x)
                cumulative += p_x
            
            results.append(x)
        
        return results
    
    @staticmethod
    def geometric(u_list: List[float], p: float) -> List[int]:
        """
        Genera una muestra de Geométrica(p).
        X = número de fracasos antes del primer éxito.
        
        Args:
            u_list: Lista de números U(0,1)
            p: Probabilidad de éxito (0 < p <= 1)
        
        Returns:
            Lista de valores enteros >= 0
        
        Fórmula: X = floor(ln(1-U) / ln(1-p))
        """
        if not 0 < p <= 1:
            raise GeneratorValidationError(
                f"La probabilidad 'p' ({p}) debe estar en (0, 1]."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        results = []
        for u in u_list:
            u_safe = max(min(u, 1.0 - 1e-12), 1e-12)

            x = math.floor(math.log(1.0 - u_safe) / math.log(1.0 - p))
            x = max(x, 0)
            results.append(x)
        
        return results
    
    @staticmethod
    def negative_binomial(u_list: List[float], r: int, p: float) -> List[int]:
        """
        Genera una muestra de Binomial Negativa(r, p).
        X = número de ensayos hasta obtener r éxitos.
        
        Args:
            u_list: Lista de números U(0,1)
            r: Número de éxitos requeridos (r > 0)
            p: Probabilidad de éxito (0 < p <= 1)
        
        Returns:
            Lista de valores enteros >= r
        
        Método: Suma de r variables Geométricas independientes
        """
        if r <= 0:
            raise GeneratorValidationError(
                f"El número de éxitos 'r' ({r}) debe ser mayor que 0."
            )
        if not 0 < p <= 1:
            raise GeneratorValidationError(
                f"La probabilidad 'p' ({p}) debe estar en (0, 1]."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        results = []
        # Necesitamos r números uniformes por cada observación
        for i in range(0, len(u_list), r):
            batch = u_list[i:i+r]
            if len(batch) < r:
                break
            
            # Suma de r geométricas independientes
            total = 0
            for u in batch:
                u_safe = max(min(u, 1.0 - 1e-12), 1e-12)
                x = math.ceil(math.log(1 - u_safe) / math.log(1 - p))
                total += max(x, 1)
            results.append(total)
        
        return results
    
    @staticmethod
    def hypergeometric(
        u_list: List[float], 
        N: int, 
        K: int, 
        n: int
    ) -> List[int]:
        """
        Genera una muestra de Hipergeométrica(N, K, n).
        X = número de éxitos en n extracciones sin reemplazo de una población 
        de tamaño N con K éxitos.
        
        Args:
            u_list: Lista de números U(0,1)
            N: Tamaño de la población
            K: Número de éxitos en la población
            n: Tamaño de la muestra
        
        Returns:
            Lista de valores entre max(0, n-(N-K)) y min(n, K)
        
        Método: Muestreo secuencial sin reemplazo (se consume un número uniforme por extracción)
        """
        if N <= 0:
            raise GeneratorValidationError(f"El tamaño de población 'N' ({N}) debe ser mayor que 0.")
        if not 0 <= K <= N:
            raise GeneratorValidationError(
                f"El número de éxitos 'K' ({K}) debe estar en [0, {N}]."
            )
        if not 0 <= n <= N:
            raise GeneratorValidationError(
                f"El tamaño de muestra 'n' ({n}) debe estar en [0, {N}]."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        results = []
        # Se consume un número uniforme por cada extracción sin reemplazo
        for i in range(0, len(u_list), n):
            batch = u_list[i:i+n]
            if len(batch) < n:
                break
            
            successes = 0
            remaining_N = N
            remaining_K = K
            
            for u in batch:
                p_success = remaining_K / remaining_N if remaining_N > 0 else 0.0
                if u < p_success:
                    successes += 1
                    remaining_K -= 1
                remaining_N -= 1
            
            results.append(successes)
        
        return results

    @staticmethod
    def uniform_discrete(u_list: List[float], i: int, j: int) -> List[int]:
        """
        Genera una muestra de Uniforme Discreta UD(i, j).
        """
        if i >= j:
            raise GeneratorValidationError(
                f"El límite inferior 'i' ({i}) debe ser menor que el límite superior 'j' ({j})."
            )
        if not validate_uniform_sequence(u_list):
            raise GeneratorValidationError("La secuencia debe estar en [0, 1).")
        
        return [i + math.floor(u * (j - i + 1)) for u in u_list]