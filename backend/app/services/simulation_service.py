from app.adapter.api.schema import (
    SimulationRequest,
    SimulationResponse,
    TestResult,
    DistributionTestResult,
    DiscreteStatsResponse,
    DiscreteHistogramPoint,
)
from app.domain.exceptions import GeneratorValidationError
from app.domain.generators import (
    LCGenerator,
    MCGenerator,
    MidSquareGenerator,
    ContinuousDistributionGenerator,
    DiscreteDistributionGenerator,
)
from app.domain.stats import ContinuousStatsCalculator, DiscreteStatsCalculator
from app.domain.validators import MeanTest, VarianceTest, KSTest, RunsTest


class SimulationService:
    @staticmethod
    def _resolve_distribution(request: SimulationRequest):
        """Resuelve el tipo y nombre de la distribución a transformar."""
        dist_type = request.distribution_type
        dist_name = request.distribution_name

        if not dist_type:
            if request.continuous_dist and request.continuous_dist.lower() != "none":
                dist_type = "continuous"
                dist_name = request.continuous_dist
            elif request.discrete_dist:
                dist_type = "discrete"
                dist_name = request.discrete_dist

        dist_type = dist_type.lower() if dist_type else "none"
        dist_name = dist_name.lower() if dist_name else "none"
        return dist_type, dist_name

    @staticmethod
    def _build_distribution_tests(
        alpha: float,
        values,
        theo_mean: float,
        theo_var: float,
        cdf,
        pmf=None,
    ) -> DistributionTestResult:
        """Aplica las cuatro pruebas estadísticas adaptadas a la distribución transformada."""
        mean_lims, mean_stat, mean_passed = MeanTest(
            alpha, expected_mean=theo_mean, expected_variance=theo_var
        ).test(values)

        var_lims, var_stat, var_passed = VarianceTest(
            alpha, expected_variance=theo_var
        ).test(values)

        ks_lims, ks_stat, ks_passed = KSTest(alpha, cdf=cdf, pmf=pmf).test(values)

        streak_lims, streak_stat, streak_passed = RunsTest(
            alpha, threshold=theo_mean
        ).test(values)

        return DistributionTestResult(
            mean_test=TestResult(
                lower_limit=mean_lims[0],
                upper_limit=mean_lims[1],
                statistic=mean_stat,
                passed=mean_passed,
            ),
            variance_test=TestResult(
                lower_limit=var_lims[0],
                upper_limit=var_lims[1],
                statistic=var_stat,
                passed=var_passed,
            ),
            ks_test=TestResult(
                lower_limit=ks_lims[0],
                upper_limit=ks_lims[1],
                statistic=ks_stat,
                passed=ks_passed,
            ),
            streak_test=TestResult(
                lower_limit=streak_lims[0],
                upper_limit=streak_lims[1],
                statistic=streak_stat,
                passed=streak_passed,
            ),
        )

    @staticmethod
    def run_simulation(request: SimulationRequest) -> SimulationResponse:
        """
        Orquesta el flujo completo de la simulación:
        1. Identifica el método generador y genera la secuencia U(0,1).
        2. Ejecuta las cuatro pruebas estadísticas sobre la secuencia generada.
        3. Si se solicita, genera la variable aleatoria elegida (continua o discreta),
           le aplica las cuatro pruebas estadísticas y calcula sus estadísticos e histograma.
        4. Empaqueta los resultados en el esquema de respuesta.
        """
        # 1. Generación de la secuencia de números pseudoaleatorios
        method = request.method.lower()

        if method == "lcg":
            if request.a is None or request.c is None or request.m is None:
                raise GeneratorValidationError(
                    "Para el método congruencial lineal (LCG) se requieren los parámetros 'a', 'c' y 'm'."
                )
            generator = LCGenerator(
                semilla=request.semilla,
                a=request.a,
                c=request.c,
                m=request.m,
            )
        elif method == "mcg":
            if request.a is None or request.m is None:
                raise GeneratorValidationError(
                    "Para el método congruencial multiplicativo (MCG) se requieren los parámetros 'a' y 'm'."
                )
            generator = MCGenerator(
                semilla=request.semilla,
                a=request.a,
                m=request.m,
            )
        elif method == "mid_square":
            generator = MidSquareGenerator(
                semilla=request.semilla,
                digits=request.digits,
            )
        else:
            raise GeneratorValidationError(
                f"Método de generación desconocido: '{request.method}'. Los métodos válidos son 'lcg', 'mcg' y 'mid_square'."
            )

        numbers = generator.generate(request.n)

        # 2. Ejecución de las pruebas estadísticas (si hay suficientes números)
        if len(numbers) < 2:
            raise GeneratorValidationError(
                "Se requieren generar al menos 2 números para poder calcular las pruebas estadísticas (especialmente varianza)."
            )

        mean_lims, mean_stat, mean_passed = MeanTest(request.alpha).test(numbers)
        mean_res = TestResult(
            lower_limit=mean_lims[0],
            upper_limit=mean_lims[1],
            statistic=mean_stat,
            passed=mean_passed,
        )

        var_lims, var_stat, var_passed = VarianceTest(request.alpha).test(numbers)
        var_res = TestResult(
            lower_limit=var_lims[0],
            upper_limit=var_lims[1],
            statistic=var_stat,
            passed=var_passed,
        )

        ks_lims, ks_stat, ks_passed = KSTest(request.alpha).test(numbers)
        ks_res = TestResult(
            lower_limit=ks_lims[0],
            upper_limit=ks_lims[1],
            statistic=ks_stat,
            passed=ks_passed,
        )

        streak_lims, streak_stat, streak_passed = RunsTest(request.alpha).test(numbers)
        streak_res = TestResult(
            lower_limit=streak_lims[0],
            upper_limit=streak_lims[1],
            statistic=streak_stat,
            passed=streak_passed,
        )

        # 3. Generación de Variable Aleatoria (Continua o Discreta)
        continuous_vals = None
        c_stats = None
        hist_data = None
        dist_tests = None

        discrete_vals = None
        d_stats = None
        d_hist_data = None

        dist_type, dist_name = SimulationService._resolve_distribution(request)

        # 3a. Generación de Variable Aleatoria Continua
        if dist_type == "continuous":
            params = request.dist_params or {}

            if dist_name == "uniform":
                a_val = float(params.get("a", 0.0))
                b_val = float(params.get("b", 1.0))
                continuous_vals = ContinuousDistributionGenerator.uniform(
                    numbers, a_val, b_val
                )
            elif dist_name == "exponential":
                lambd = float(params.get("lambd", 1.0))
                continuous_vals = ContinuousDistributionGenerator.exponential(
                    numbers, lambd
                )
            elif dist_name == "normal":
                mean_val = float(params.get("mean", 0.0))
                std_dev = float(params.get("std_dev", 1.0))
                continuous_vals = ContinuousDistributionGenerator.normal(
                    numbers, mean_val, std_dev
                )
            elif dist_name == "weibull":
                alpha_val = float(params.get("alpha", 1.0))
                beta_val = float(params.get("beta", 1.0))
                continuous_vals = ContinuousDistributionGenerator.weibull(
                    numbers, alpha_val, beta_val
                )
            else:
                raise GeneratorValidationError(
                    f"Distribución continua no soportada: '{request.distribution_name}'. "
                    "Válidas: 'uniform', 'exponential', 'normal', 'weibull'."
                )

            c_stats, hist_data = ContinuousStatsCalculator.calculate_stats(
                continuous_vals, dist_name, params
            )
            dist_tests = SimulationService._build_distribution_tests(
                request.alpha,
                continuous_vals,
                float(c_stats["theoretical_mean"]),
                float(c_stats["theoretical_variance"]),
                ContinuousStatsCalculator.get_cdf(dist_name, params),
            )

        # 3b. Generación de Variable Aleatoria Discreta
        elif dist_type == "discrete":
            params = request.dist_params or {}

            if dist_name == "bernoulli":
                p = float(params.get("p", 0.5))
                discrete_vals = DiscreteDistributionGenerator.bernoulli(numbers, p)
            elif dist_name == "binomial":
                n = int(params.get("n", 10))
                p = float(params.get("p", 0.5))
                discrete_vals = DiscreteDistributionGenerator.binomial(numbers, n, p)
            elif dist_name == "poisson":
                lambd = float(params.get("lambda", 1.0))
                discrete_vals = DiscreteDistributionGenerator.poisson(numbers, lambd)
            elif dist_name == "geometric":
                p = float(params.get("p", 0.5))
                discrete_vals = DiscreteDistributionGenerator.geometric(numbers, p)
            elif dist_name == "negative_binomial":
                r = int(params.get("r", 5))
                p = float(params.get("p", 0.5))
                discrete_vals = DiscreteDistributionGenerator.negative_binomial(
                    numbers, r, p
                )
            elif dist_name == "hypergeometric":
                N = int(params.get("N", 100))
                K = int(params.get("K", 50))
                n = int(params.get("n_sample", 10))
                discrete_vals = DiscreteDistributionGenerator.hypergeometric(
                    numbers, N, K, n
                )
            else:
                raise GeneratorValidationError(
                    f"Distribución discreta no soportada: '{request.distribution_name}'. "
                    "Válidas: 'bernoulli', 'binomial', 'poisson', 'geometric', "
                    "'negative_binomial', 'hypergeometric'."
                )

            if not discrete_vals:
                raise GeneratorValidationError(
                    "La secuencia base generada no contiene suficientes números para "
                    "obtener al menos una observación de la distribución discreta solicitada."
                )

            stats_dict = DiscreteStatsCalculator.calculate_stats(
                discrete_vals, dist_name, params
            )

            if len(discrete_vals) < 2:
                raise GeneratorValidationError(
                    "Se requieren al menos 2 observaciones de la distribución discreta "
                    "para aplicar las pruebas estadísticas."
                )

            dist_tests = SimulationService._build_distribution_tests(
                request.alpha,
                discrete_vals,
                float(stats_dict["theoretical_mean"]),
                float(stats_dict["theoretical_variance"]),
                DiscreteStatsCalculator.get_cdf(dist_name, params),
                pmf=DiscreteStatsCalculator.get_pmf(dist_name, params),
            )

            d_stats = DiscreteStatsResponse(
                sample_size=stats_dict["sample_size"],
                empirical_mean=stats_dict["empirical_mean"],
                empirical_variance=stats_dict["empirical_variance"],
                theoretical_mean=stats_dict["theoretical_mean"],
                theoretical_variance=stats_dict["theoretical_variance"],
                mean_diff=stats_dict["mean_diff"],
                variance_diff=stats_dict["variance_diff"],
                frequencies=stats_dict["frequencies"],
                relative_frequencies=stats_dict["relative_frequencies"],
                unique_values=stats_dict["unique_values"],
                min_value=stats_dict["min_value"],
                max_value=stats_dict["max_value"],
                mode=stats_dict["mode"],
            )

            hist_data_list = DiscreteStatsCalculator.create_histogram_data(
                discrete_vals, stats_dict["frequencies"]
            )
            d_hist_data = [
                DiscreteHistogramPoint(
                    value=item["value"],
                    count=item["count"],
                    relative_frequency=item["relative_frequency"],
                    cumulative_count=item["cumulative_count"],
                    cumulative_relative=item["cumulative_relative"],
                )
                for item in hist_data_list
            ]

        # 4. Construcción y retorno de la respuesta estructurada
        return SimulationResponse(
            numbers=numbers,
            mean_test=mean_res,
            variance_test=var_res,
            ks_test=ks_res,
            streak_test=streak_res,
            distribution_tests=dist_tests,
            # Datos continuos
            continuous_values=continuous_vals,
            continuous_stats=c_stats,
            histogram=hist_data,
            # Datos discretos
            discrete_values=discrete_vals,
            discrete_stats=d_stats,
            discrete_histogram=d_hist_data,
        )
