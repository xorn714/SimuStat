from app.adapter.api.schema import SimulationRequest, SimulationResponse, TestResult
from app.domain.generators import (
    linear_congruential,
    multiplicative_congruential,
    mid_square,
    uniform_continuous,
    exponential_continuous,
    normal_continuous,
    weibull_continuous,
    GeneratorValidationError
)
from app.domain.validators import mean_test, variance_test, ks_test, runs_test
from app.domain.continuous_stats import calculate_continuous_stats


class SimulationService:
    @staticmethod
    def run_simulation(request: SimulationRequest) -> SimulationResponse:
        """
        Orquesta el flujo completo de la simulación:
        1. Identifica el método generador y genera la secuencia U(0,1).
        2. Ejecuta las cuatro pruebas estadísticas sobre la secuencia generada.
        3. Si se solicita, genera la variable aleatoria continua elegida y calcula sus estadísticos e histograma.
        4. Empaqueta los resultados en el esquema de respuesta.
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

        # Prueba de Rachas
        streak_lims, streak_stat, streak_passed = runs_test(numbers, request.alpha)
        streak_res = TestResult(
            lower_limit=streak_lims[0],
            upper_limit=streak_lims[1],
            statistic=streak_stat,
            passed=streak_passed
        )

        # 3. Generación de Variable Aleatoria Continua (opcional)
        continuous_vals = None
        c_stats = None
        hist_data = None

        c_dist = request.continuous_dist.lower() if request.continuous_dist else "none"
        if c_dist != "none":
            params = request.dist_params or {}
            if c_dist == "uniform":
                a_val = float(params.get("a", 0.0))
                b_val = float(params.get("b", 1.0))
                continuous_vals = uniform_continuous(numbers, a_val, b_val)
            elif c_dist == "exponential":
                lambd = float(params.get("lambd", 1.0))
                continuous_vals = exponential_continuous(numbers, lambd)
            elif c_dist == "normal":
                mean_val = float(params.get("mean", 0.0))
                std_dev = float(params.get("std_dev", 1.0))
                continuous_vals = normal_continuous(numbers, mean_val, std_dev)
            elif c_dist == "weibull":
                alpha_val = float(params.get("alpha", 1.0))
                beta_val = float(params.get("beta", 1.0))
                continuous_vals = weibull_continuous(numbers, alpha_val, beta_val)
            else:
                raise GeneratorValidationError(
                    f"Distribución continua no soportada: '{request.continuous_dist}'. Válidas: 'uniform', 'exponential', 'normal', 'weibull'."
                )

            c_stats, hist_data = calculate_continuous_stats(continuous_vals, c_dist, params)

        # 4. Construcción y retorno de la respuesta estructurada
        return SimulationResponse(
            numbers=numbers,
            mean_test=mean_res,
            variance_test=var_res,
            ks_test=ks_res,
            streak_test=streak_res,
            continuous_values=continuous_vals,
            continuous_stats=c_stats,
            histogram=hist_data
        )


