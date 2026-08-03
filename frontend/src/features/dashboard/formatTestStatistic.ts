export function formatTestStatistic(value: number | null | undefined): string {
  if (value == null) return '∞'
  if (!Number.isFinite(value)) return value > 0 ? '∞' : '-∞'
  return value.toFixed(6)
}
