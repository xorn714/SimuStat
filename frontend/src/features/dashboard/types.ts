export interface TestResult {
  lower_limit: number
  upper_limit: number
  statistic: number
  passed: boolean
}

export interface SimulationData {
  numbers: number[]
  mean_test: TestResult
  variance_test: TestResult
  ks_test: TestResult
  streak_test: TestResult
}

