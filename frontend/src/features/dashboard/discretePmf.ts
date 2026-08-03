export type DiscretePmfParams = {
  p?: number
  n?: number
  r?: number
  N?: number
  K?: number
  n_sample?: number
  lambda?: number
}

function combination(n: number, k: number): number {
  if (k < 0 || k > n) return 0
  let result = 1
  for (let i = 0; i < k; i++) {
    result *= (n - i) / (i + 1)
  }
  return Math.round(result)
}

export function getDiscretePmf(distName: string, params: DiscretePmfParams) {
  const p = params.p ?? 0.5

  switch (distName) {
    case 'bernoulli':
      return (k: number) => (k === 0 ? 1 - p : k === 1 ? p : 0)

    case 'binomial': {
      const n = params.n ?? 10
      return (k: number) =>
        0 <= k && k <= n ? combination(n, k) * p ** k * (1 - p) ** (n - k) : 0
    }

    case 'poisson': {
      const lambda = params.lambda ?? 1
      return (k: number) => {
        if (k < 0) return 0
        let term = Math.exp(-lambda)
        for (let i = 1; i <= k; i++) term *= lambda / i
        return term
      }
    }

    case 'geometric':
      return (k: number) => (k >= 1 ? (1 - p) ** (k - 1) * p : 0)

    case 'negative_binomial': {
      const r = params.r ?? 5
      return (k: number) =>
        k >= r ? combination(k - 1, r - 1) * p ** r * (1 - p) ** (k - r) : 0
    }

    case 'hypergeometric': {
      const N = params.N ?? 100
      const K = params.K ?? 50
      const n = params.n_sample ?? 10
      const denom = combination(N, n)
      return (k: number) => {
        const lo = Math.max(0, n - (N - K))
        const hi = Math.min(n, K)
        if (k < lo || k > hi || denom === 0) return 0
        return (combination(K, k) * combination(N - K, n - k)) / denom
      }
    }

    default:
      return () => 0
  }
}
