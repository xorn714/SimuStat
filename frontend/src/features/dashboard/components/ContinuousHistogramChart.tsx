import React from 'react'
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
import type { HistogramData } from '../types'

interface ContinuousHistogramChartProps {
  histogram: HistogramData
}

export const ContinuousHistogramChart: React.FC<ContinuousHistogramChartProps> = ({ histogram }) => {
  const chartData = histogram.bins.map((b) => ({
    bin: b.bin,
    mid: b.mid,
    count: b.count,
    Empírica: b.empirical_density,
    Teórica: b.theoretical_density,
  }))

  return (
    <div className="bg-[#171F33]/60 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white font-headline">Histograma y Función de Densidad (PDF)</h3>
          <p className="text-xs text-slate-400">Comparación de la densidad empírica simulada vs la curva teórica esperada</p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold rounded-full font-label">
          {histogram.bins.length} Bins
        </span>
      </div>

      <div className="h-72 w-full pt-4">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
            <XAxis
              dataKey="bin"
              stroke="#64748B"
              fontSize={10}
              tickLine={false}
              angle={-20}
              textAnchor="end"
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
            <Bar dataKey="Empírica" fill="#10B981" radius={[4, 4, 0, 0]} opacity={0.7} />
            <Line type="monotone" dataKey="Teórica" stroke="#38BDF8" strokeWidth={2.5} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
