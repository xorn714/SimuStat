# pyrefly: ignore [missing-import]
import pytest
from app.domain.exceptions import StatsCalculationError
from app.domain.stats import DiscreteStatsCalculator


def test_calculate_stats_bernoulli():
    values = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    stats = DiscreteStatsCalculator.calculate_stats(values, "bernoulli", {"p": 0.3})

    assert stats["sample_size"] == 10
    assert stats["empirical_mean"] == pytest.approx(0.3)
    assert stats["theoretical_mean"] == pytest.approx(0.3)
    assert stats["theoretical_variance"] == pytest.approx(0.21)
    assert stats["mode"] == 0
    assert stats["min_value"] == 0
    assert stats["max_value"] == 1
    assert stats["unique_values"] == 2
    assert stats["frequencies"] == {0: 7, 1: 3}


def test_calculate_stats_binomial():
    values = [5, 5, 5, 5, 5]
    stats = DiscreteStatsCalculator.calculate_stats(values, "binomial", {"n": 10, "p": 0.5})

    assert stats["empirical_mean"] == pytest.approx(5.0)
    assert stats["theoretical_mean"] == pytest.approx(5.0)
    assert stats["empirical_variance"] == pytest.approx(0.0)
    assert stats["theoretical_variance"] == pytest.approx(2.5)


def test_calculate_stats_uniform_discrete():
    # Según UD(i, j) del libro: media = (i+j)/2, var = ((j-i+1)^2 - 1)/12
    values = [1, 2, 3, 4, 5, 6]
    stats = DiscreteStatsCalculator.calculate_stats(values, "uniform_discrete", {"i": 1, "j": 6})

    assert stats["theoretical_mean"] == pytest.approx(3.5)
    assert stats["theoretical_variance"] == pytest.approx((36 - 1) / 12.0)  # 35/12 = 2.916667


def test_calculate_stats_poisson_geometric_negative_binomial():
    # Poisson: media = lambda, var = lambda (García Dunna pág. 10 y 308)
    poisson = DiscreteStatsCalculator.calculate_stats([2, 3, 3, 4], "poisson", {"lambda": 3.0})
    assert poisson["theoretical_mean"] == pytest.approx(3.0)
    assert poisson["theoretical_variance"] == pytest.approx(3.0)

    # Geométrica según García Dunna pág. 10 y 307: rango {0, 1, ...}, media = (1-p)/p, var = (1-p)/p^2
    geometric = DiscreteStatsCalculator.calculate_stats([0, 1, 2], "geometric", {"p": 0.5})
    assert geometric["theoretical_mean"] == pytest.approx(1.0)
    assert geometric["theoretical_variance"] == pytest.approx(2.0)

    # Binomial Negativa: r éxitos, probabilidad p
    neg_bin = DiscreteStatsCalculator.calculate_stats([8, 9, 10], "negative_binomial", {"r": 5, "p": 0.6})
    assert neg_bin["theoretical_mean"] == pytest.approx(5 / 0.6)
    assert neg_bin["theoretical_variance"] == pytest.approx(5 * 0.4 / 0.36)


def test_calculate_stats_empty():
    with pytest.raises(StatsCalculationError):
        DiscreteStatsCalculator.calculate_stats([], "bernoulli", {"p": 0.5})


def test_create_histogram_data():
    values = [0, 1, 1]
    data = DiscreteStatsCalculator.create_histogram_data(values, {0: 1, 1: 2})

    assert data[0] == {
        "value": 0,
        "count": 1,
        "relative_frequency": 1 / 3,
        "cumulative_count": 1,
        "cumulative_relative": pytest.approx(0.3333, abs=1e-4),
    }
    assert data[1]["cumulative_count"] == 3
    assert data[1]["cumulative_relative"] == pytest.approx(1.0)


def test_get_cdf_discrete():
    binomial = DiscreteStatsCalculator.get_cdf("binomial", {"n": 10, "p": 0.5})
    assert binomial(-1) == 0.0
    assert binomial(0) == pytest.approx(0.5 ** 10)
    assert binomial(5) == pytest.approx(0.623047, abs=1e-5)
    assert binomial(10) == 1.0
    assert binomial(100) == 1.0

    poisson = DiscreteStatsCalculator.get_cdf("poisson", {"lambda": 3.0})
    assert poisson(2) == pytest.approx(0.42319, abs=1e-5)

    # Geométrica según fórmula F(x) = 1 - (1-p)^(floor(x)+1) del libro (pág. 307)
    geometric = DiscreteStatsCalculator.get_cdf("geometric", {"p": 0.5})
    assert geometric(-1) == 0.0
    assert geometric(0) == pytest.approx(0.5)
    assert geometric(1) == pytest.approx(0.75)

    neg_bin = DiscreteStatsCalculator.get_cdf("negative_binomial", {"r": 5, "p": 0.6})
    assert neg_bin(4) == 0.0
    assert neg_bin(5) == pytest.approx(0.6 ** 5)

    hyper = DiscreteStatsCalculator.get_cdf("hypergeometric", {"N": 10, "K": 4, "n": 5})
    assert hyper(0) == pytest.approx(6 / 252)
    assert hyper(4) == pytest.approx(1.0)


def test_get_pmf_discrete():
    binomial = DiscreteStatsCalculator.get_pmf("binomial", {"n": 10, "p": 0.5})
    assert binomial(5) == pytest.approx(252 / 1024)
    assert binomial(11) == 0.0

    poisson = DiscreteStatsCalculator.get_pmf("poisson", {"lambda": 3.0})
    assert poisson(2) == pytest.approx(0.224042, abs=1e-5)

    bernoulli = DiscreteStatsCalculator.get_pmf("bernoulli", {"p": 0.4})
    assert bernoulli(0) == pytest.approx(0.6)
    assert bernoulli(1) == pytest.approx(0.4)
    assert bernoulli(2) == 0.0

    # Geométrica según p(x) = p(1-p)^x para x = 0, 1, 2, ... (pág. 307)
    geometric = DiscreteStatsCalculator.get_pmf("geometric", {"p": 0.4})
    assert geometric(0) == pytest.approx(0.4)
    assert geometric(1) == pytest.approx(0.24)
