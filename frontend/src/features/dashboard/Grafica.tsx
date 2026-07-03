import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface GraficaProps {
  numbers: number[]
}

export const Grafica: React.FC<GraficaProps> = ({ numbers }) => {
  const data = numbers.map((value, index) => ({
    index,
    value: Number(value.toFixed(4)),
  }))

  return (
    <div className="p-6 rounded-2xl border border-slate-800 bg-[#171F33]/20">
      <h3 className="text-lg font-bold text-white font-headline mb-4">
        Secuencia de Números Generados
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="index"
            stroke="#64748b"
            tick={{ fontSize: 11 }}
            label={{ value: 'Índice', position: 'insideBottom', offset: -5, style: { fill: '#64748b', fontSize: 11 } }}
          />
          <YAxis
            domain={[0, 1]}
            stroke="#64748b"
            tick={{ fontSize: 11 }}
            label={{ value: 'Valor', angle: -90, position: 'insideLeft', style: { fill: '#64748b', fontSize: 11 } }}
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
          <Line
            type="monotone"
            dataKey="value"
            stroke="#4CD7F6"
            strokeWidth={1.5}
            dot={false}
            activeDot={{ r: 3, fill: '#4CD7F6' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
