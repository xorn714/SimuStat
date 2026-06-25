from app.adapter.api.schema import SimulationRequest, SimulationResponse, TestResult
from app.domain.generators import (
    linear_congruential,
    multiplicative_congruential,
    mid_square,
    GeneratorValidationError
)
from app.domain.validators import mean_test, variance_test, ks_test


class SimulationService:
    @staticmethod
    def run_simulation(request: SimulationRequest) -> SimulationResponse:
        """
        Orquesta el flujo completo de la simulación:
        1. Identifica el método generador y genera la secuencia.
        2. Ejecuta las tres pruebas estadísticas sobre la secuencia generada.
        3. Empaqueta los resultados en el esquema de respuesta.
        """
        # 1. Generación de la secuencia de números pseudoaleatorios
        method = request.method.lower()

        if method == "lcg":
            if request.a is None or request.c is None or request.m is None:
                raise GeneratorValidationError(
                    "Para el método congruencial lineal (LCG) se requieren los parámetros 'a', 'c' y 'm'."
                )
            numbers = linear_congruential(
                semilla=request.semilla,
                a=request.a,
                c=request.c,
                m=request.m,
                n=request.n
            )
        elif method == "mcg":
            if request.a is None or request.m is None:
                raise GeneratorValidationError(
                    "Para el método congruencial multiplicativo (MCG) se requieren los parámetros 'a' y 'm'."
                )
            numbers = multiplicative_congruential(
                semilla=request.semilla,
                a=request.a,
                m=request.m,
                n=request.n
            )
        elif method == "mid_square":
            numbers = mid_square(
                semilla=request.semilla,
                n=request.n,
                digits=request.digits
            )
        else:
            raise GeneratorValidationError(
                f"Método de generación desconocido: '{request.method}'. Los métodos válidos son 'lcg', 'mcg' y 'mid_square'."
            )

        # 2. Ejecución de las pruebas estadísticas (si hay suficientes números)
        # Nota: La prueba de varianza requiere al menos 2 números (ddof=1)
        if len(numbers) < 2:
            raise GeneratorValidationError(
                "Se requieren generar al menos 2 números para poder calcular las pruebas estadísticas (especialmente varianza)."
            )

        # Prueba de Medias
        mean_lims, mean_stat, mean_passed = mean_test(numbers, request.alpha)
        mean_res = TestResult(
            lower_limit=mean_lims[0],
            upper_limit=mean_lims[1],
            statistic=mean_stat,
            passed=mean_passed
        )

        # Prueba de Varianzas
        var_lims, var_stat, var_passed = variance_test(numbers, request.alpha)
        var_res = TestResult(
            lower_limit=var_lims[0],
            upper_limit=var_lims[1],
            statistic=var_stat,
            passed=var_passed
        )

        # Prueba KS
        ks_lims, ks_stat, ks_passed = ks_test(numbers, request.alpha)
        ks_res = TestResult(
            lower_limit=ks_lims[0],
            upper_limit=ks_lims[1],
            statistic=ks_stat,
            passed=ks_passed
        )

        # 3. Construcción y retorno de la respuesta estructurada
        return SimulationResponse(
            numbers=numbers,
            mean_test=mean_res,
            variance_test=var_res,
            ks_test=ks_res
        )
