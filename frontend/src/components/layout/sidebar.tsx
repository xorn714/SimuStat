import React, { useState } from 'react'
import { LayoutDashboard, Play, History, Settings2, Calculator } from 'lucide-react'

export type SidebarTabType = 'dashboard' | 'simulacion' | 'historial'
export type GeneratorMethod = 'lineal' | 'multiplicativo' | 'cuadrados_medios'

export interface GeneratorParams {
  method: GeneratorMethod
  seed: number
  a?: number
  c?: number
  m?: number
  digits?: number
  quantity: number
}

interface SidebarProps {
  activeTab: SidebarTabType
  setActiveTab: (tab: SidebarTabType) => void
  onGenerate: (params: GeneratorParams) => void
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  onGenerate,
}) => {
  const [method, setMethod] = useState<GeneratorMethod>('lineal')
  const [seed, setSeed] = useState<string>('37')
  const [a, setA] = useState<string>('19')
  const [c, setC] = useState<string>('33')
  const [m, setM] = useState<string>('100')
  const [digits, setDigits] = useState<string>('4')
  const [quantity, setQuantity] = useState<string>('100')

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault()
    const params: GeneratorParams = {
      method,
      seed: Number(seed),
      quantity: Number(quantity),
    }

    if (method === 'lineal' || method === 'multiplicativo') {
      params.a = Number(a)
      params.m = Number(m)
    }

    if (method === 'lineal') {
      params.c = Number(c)
    }

    if (method === 'cuadrados_medios') {
      params.digits = Number(digits)
    }

    onGenerate(params)
  }

  return (
    <aside className="w-80 border-r border-slate-800 bg-[#171F33]/40 backdrop-blur-md flex flex-col h-[calc(100vh-4rem)] sticky top-16 scrollbar-none">
      {/* Sidebar Navigation */}
      <div className="p-4 space-y-1">
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest font-label px-3 mb-2">Navegación</h3>

        <button
          onClick={() => setActiveTab('dashboard')}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all cursor-pointer ${activeTab === 'dashboard'
              ? 'bg-[#4EDEA3]/10 text-[#4EDEA3]'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/30'
            }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          Dashboard
        </button>

        <button
          onClick={() => setActiveTab('simulacion')}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all cursor-pointer ${activeTab === 'simulacion'
              ? 'bg-[#4EDEA3]/10 text-[#4EDEA3]'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/30'
            }`}
        >
          <Play className="w-4 h-4" />
          Simulación
        </button>

        <button
          onClick={() => setActiveTab('historial')}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all cursor-pointer ${activeTab === 'historial'
              ? 'bg-[#4EDEA3]/10 text-[#4EDEA3]'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/30'
            }`}
        >
          <History className="w-4 h-4" />
          Historial
        </button>
      </div>

      <div className="border-t border-slate-800/60 my-2" />

      {/* Algorithm Config Section */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-none">
        <div className="flex items-center gap-2 px-3">
          <Settings2 className="w-4 h-4 text-primary" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-widest font-label">Algoritmo</h3>
        </div>

        <form onSubmit={handleGenerate} className="space-y-4 px-3">
          {/* Method Select */}
          <div className="space-y-1.5">
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Método</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value as GeneratorMethod)}
              className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors cursor-pointer"
            >
              <option value="lineal">Congruencia Lineal</option>
              <option value="multiplicativo">Congruencia Multiplicativa</option>
              <option value="cuadrados_medios">Cuadrado Medio</option>
            </select>
          </div>

          {/* Conditional Inputs */}
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Semilla (X₀)</label>
                <input
                  type="number"
                  value={seed}
                  onChange={(e) => setSeed(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Cantidad (N)</label>
                <input
                  type="number"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
                  required
                />
              </div>
            </div>

            {/* If Lineal or Multiplicativo */}
            {(method === 'lineal' || method === 'multiplicativo') && (
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Constante a</label>
                  <input
                    type="number"
                    value={a}
                    onChange={(e) => setA(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
                    required
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Módulo m</label>
                  <input
                    type="number"
                    value={m}
                    onChange={(e) => setM(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
                    required
                  />
                </div>
              </div>
            )}

            {/* If Lineal (requires c) */}
            {method === 'lineal' && (
              <div className="space-y-1.5">
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Constante c</label>
                <input
                  type="number"
                  value={c}
                  onChange={(e) => setC(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
                  required
                />
              </div>
            )}

            {/* If Cuadrados Medios */}
            {method === 'cuadrados_medios' && (
              <div className="space-y-1.5">
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Cantidad de Dígitos</label>
                <select
                  value={digits}
                  onChange={(e) => setDigits(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors cursor-pointer"
                >
                  <option value="4">4 Dígitos</option>
                  <option value="6">6 Dígitos</option>
                  <option value="8">8 Dígitos</option>
                </select>
              </div>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-primary to-tertiary hover:opacity-90 text-neutral font-bold py-2.5 px-4 rounded-xl shadow-lg shadow-primary/10 transition-all duration-200 active:scale-[0.98] cursor-pointer flex items-center justify-center gap-2 text-xs"
          >
            <Calculator className="w-3.5 h-3.5" />
            Generar
          </button>
        </form>
      </div>
    </aside>
  )
}
