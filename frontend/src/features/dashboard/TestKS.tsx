import React from 'react'
import type { TestResult } from './types'
import { formatTestStatistic } from './formatTestStatistic'

interface TestKSProps {
  result: TestResult | null
}

export const TestKS: React.FC<TestKSProps> = ({ result }) => {
  const passed = result?.passed ?? false

  return (
    <div
      className={`p-6 rounded-2xl border transition-colors ${
        result
          ? passed
            ? 'border-green-500/40 bg-green-500/10'
            : 'border-red-500/40 bg-red-500/10'
          : 'border-slate-800 bg-[#171F33]/20'
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white font-headline">
          Prueba Kolmogorov-Smirnov
        </h3>
        {result && (
          <span
            className={`text-xs font-bold font-label uppercase tracking-wider px-3 py-1 rounded-full ${
              passed
                ? 'text-green-400 bg-green-500/20'
                : 'text-red-400 bg-red-500/20'
            }`}
          >
            {passed ? 'PASÓ' : 'NO PASÓ'}
          </span>
        )}
      </div>

      {result ? (
        <div className="space-y-2 text-sm font-label">
          <div className="flex justify-between">
            <span className="text-slate-400">Estadístico D:</span>
            <span className={passed ? 'text-green-300' : 'text-red-300'}>
              {formatTestStatistic(result.statistic)}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Valor crítico:</span>
            <span className="text-slate-300">{result.upper_limit.toFixed(6)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Límite inferior:</span>
            <span className="text-slate-300">{result.lower_limit.toFixed(6)}</span>
          </div>
        </div>
      ) : (
        <p className="text-sm text-slate-500">
          Genere una simulación para ver el resultado.
        </p>
      )}
    </div>
  )
}
