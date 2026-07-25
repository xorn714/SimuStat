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

export interface SimulationData {
  numbers: number[]
  mean_test: TestResult
  variance_test: TestResult
  ks_test: TestResult
  streak_test: TestResult
  continuous_values?: number[]
  continuous_stats?: ContinuousStats
  histogram?: HistogramData
}
