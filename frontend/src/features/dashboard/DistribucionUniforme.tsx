import React, { useMemo } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface DistribucionUniformeProps {
  numbers: number[]
  bins?: number
}

function createHistogram(data: number[], bins: number) {
  const binWidth = 1 / bins
  const counts = new Array(bins).fill(0)

  data.forEach((value) => {
    const binIndex = Math.min(Math.floor(value / binWidth), bins - 1)
    counts[binIndex]++
  })

  return counts.map((count, i) => ({
    binLabel: `${(i * binWidth).toFixed(1)}-${((i + 1) * binWidth).toFixed(1)}`,
    frecuencia: count,
  }))
}

export const DistribucionUniforme: React.FC<DistribucionUniformeProps> = ({
  numbers,
  bins = 10,
}) => {
  const histogramData = useMemo(
    () => createHistogram(numbers, bins),
    [numbers, bins]
  )

  return (
    <div className="p-6 rounded-2xl border border-slate-800 bg-[#171F33]/20">
      <h3 className="text-lg font-bold text-white font-headline mb-4">
        Distribución Uniforme
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={histogramData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="binLabel"
            stroke="#64748b"
            tick={{ fontSize: 9 }}
            interval={0}
            angle={-30}
            textAnchor="end"
          />
          <YAxis
            stroke="#64748b"
            tick={{ fontSize: 11 }}
            label={{
              value: 'Frecuencia',
              angle: -90,
              position: 'insideLeft',
              style: { fill: '#64748b', fontSize: 11 },
            }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0F172A',
              border: '1px solid #1e293b',
              borderRadius: '8px',
              fontSize: '12px',
            }}
            labelStyle={{ color: '#94a3b8' }}
          />
          <Bar dataKey="frecuencia" fill="#10B981" radius={[2, 2, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
