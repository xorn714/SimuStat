export interface TestResult {
  lower_limit: number
  upper_limit: number
  statistic: number
  passed: boolean
}

export interface ContinuousStats {
  empirical_mean: number
  theoretical_mean: number
  mean_diff: number
  empirical_variance: number
  theoretical_variance: number
  variance_diff: number
  min: number
  max: number
}

export interface HistogramBin {
  bin: string
  bin_start: number
  bin_end: number
  mid: number
  count: number
  empirical_density: number
  theoretical_density: number
}

export interface HistogramData {
  bins: HistogramBin[]
  bin_width: number
  total_count: number
}

export interface DistributionTestResult {
  mean_test: TestResult | null
  variance_test: TestResult | null
  ks_test: TestResult | null
  streak_test: TestResult | null
}

export interface DiscreteStats {
  sample_size: number
  empirical_mean: number
  empirical_variance: number
  theoretical_mean: number
  theoretical_variance: number
  mean_diff: number
  variance_diff: number
  frequencies: Record<number, number>
  relative_frequencies: Record<number, number>
  unique_values: number
  min_value: number
  max_value: number
  mode: number | null
}

export interface DiscreteHistogramPoint {
  value: number
  count: number
  relative_frequency: number
  cumulative_count: number
  cumulative_relative: number
}

export interface SimulationData {
  numbers: number[]
  mean_test: TestResult
  variance_test: TestResult
  ks_test: TestResult
  streak_test: TestResult
  continuous_values?: number[]
  continuous_stats?: ContinuousStats
  histogram?: HistogramData
  discrete_values?: number[]
  discrete_stats?: DiscreteStats
  discrete_histogram?: DiscreteHistogramPoint[]
  distribution_tests?: DistributionTestResult
}
