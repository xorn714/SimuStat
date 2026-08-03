import React from 'react'
import type { DiscreteStats } from '../types'
import { TrendingUp } from 'lucide-react'

interface DiscreteStatsCardProps {
  stats: DiscreteStats
  discreteValues?: number[]
}

export const DiscreteStatsCard: React.FC<DiscreteStatsCardProps> = ({ stats, discreteValues }) => {
  return (
    <div className="bg-[#171F33]/60 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-violet-500/10 rounded-xl border border-violet-500/20 text-violet-400">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white font-headline">Estadísticos de la Variable Discreta</h3>
            <p className="text-xs text-slate-400">Comparación entre estimaciones empíricas y parámetros teóricos</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-3 bg-[#0F172A] border border-slate-800 rounded-xl">
          <span className="block text-[10px] font-label text-slate-400 uppercase">Media Empírica</span>
          <span className="text-lg font-mono font-bold text-white">{stats.empirical_mean}</span>
        </div>
        <div className="p-3 bg-[#0F172A] border border-slate-800 rounded-xl">
          <span className="block text-[10px] font-label text-slate-400 uppercase">Media Teórica</span>
          <span className="text-lg font-mono font-bold text-violet-400">{stats.theoretical_mean}</span>
        </div>
        <div className="p-3 bg-[#0F172A] border border-slate-800 rounded-xl">
          <span className="block text-[10px] font-label text-slate-400 uppercase">Varianza Empírica</span>
          <span className="text-lg font-mono font-bold text-white">{stats.empirical_variance}</span>
        </div>
        <div className="p-3 bg-[#0F172A] border border-slate-800 rounded-xl">
          <span className="block text-[10px] font-label text-slate-400 uppercase">Varianza Teórica</span>
          <span className="text-lg font-mono font-bold text-violet-400">{stats.theoretical_variance}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-label">
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Diferencia Media:</span>
          <span className="font-mono text-slate-200">{stats.mean_diff}</span>
        </div>
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Diferencia Varianza:</span>
          <span className="font-mono text-slate-200">{stats.variance_diff}</span>
        </div>
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Mínimo (X):</span>
          <span className="font-mono text-slate-200">{stats.min_value}</span>
        </div>
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Máximo (X):</span>
          <span className="font-mono text-slate-200">{stats.max_value}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs font-label">
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Valores Distintos:</span>
          <span className="font-mono text-slate-200">{stats.unique_values}</span>
        </div>
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Moda:</span>
          <span className="font-mono text-slate-200">{stats.mode ?? '-'}</span>
        </div>
        <div className="p-2.5 bg-slate-900/50 rounded-lg border border-slate-800 flex justify-between items-center">
          <span className="text-slate-400">Tamaño Muestral:</span>
          <span className="font-mono text-slate-200">{stats.sample_size}</span>
        </div>
      </div>

      {discreteValues && discreteValues.length > 0 && (
        <div className="space-y-2 pt-2 border-t border-slate-800">
          <h4 className="text-xs font-semibold text-slate-300 font-label uppercase">Muestra de Valores Generados (Primeros 10)</h4>
          <div className="flex flex-wrap gap-2">
            {discreteValues.slice(0, 10).map((v, idx) => (
              <span key={idx} className="px-2.5 py-1 bg-[#0F172A] border border-slate-800 rounded font-mono text-xs text-violet-300">
                X_{idx + 1}: {v}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
