import React, { useMemo } from 'react'
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import type { DiscreteHistogramPoint } from '../types'
import { getDiscretePmf } from '../discretePmf'

interface DiscreteHistogramChartProps {
  histogram: DiscreteHistogramPoint[]
  distName?: string
  distParams?: Record<string, number>
}

export const DiscreteHistogramChart: React.FC<DiscreteHistogramChartProps> = ({
  histogram,
  distName,
  distParams,
}) => {
  const chartData = useMemo(() => {
    const pmf = distName ? getDiscretePmf(distName, distParams ?? {}) : () => 0
    return histogram.map((h) => ({
      value: h.value,
      count: h.count,
      'Frec. Rel. Empírica': Number(h.relative_frequency.toFixed(4)),
      'PMF Teórica': Number(pmf(h.value).toFixed(4)),
    }))
  }, [histogram, distName, distParams])

  return (
    <div className="bg-[#171F33]/60 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white font-headline">Histograma y Función de Masa de Probabilidad (PMF)</h3>
          <p className="text-xs text-slate-400">Comparación de la frecuencia relativa empírica simulada vs la probabilidad teórica esperada</p>
        </div>
        <span className="px-3 py-1 bg-violet-500/10 border border-violet-500/30 text-violet-400 text-xs font-semibold rounded-full font-label">
          {histogram.length} Valores
        </span>
      </div>

      <div className="h-72 w-full pt-4">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
            <XAxis
              dataKey="value"
              stroke="#64748B"
              fontSize={10}
              tickLine={false}
              angle={-20}
              textAnchor="end"
              interval={0}
            />
            <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0F172A',
                borderColor: '#334155',
                borderRadius: '8px',
                color: '#F8FAFC',
                fontSize: '12px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
            <Bar dataKey="Frec. Rel. Empírica" fill="#8B5CF6" radius={[4, 4, 0, 0]} opacity={0.7} />
            <Line type="monotone" dataKey="PMF Teórica" stroke="#4CD7F6" strokeWidth={2.5} dot={{ r: 3, fill: '#4CD7F6' }} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
