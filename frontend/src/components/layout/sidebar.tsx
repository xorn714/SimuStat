import React, { useState } from 'react'
import { Settings2, Calculator, Activity } from 'lucide-react'

export type GeneratorMethod = 'lineal' | 'multiplicativo' | 'cuadrados_medios'
export type ContinuousDistType = 'uniform' | 'exponential' | 'normal' | 'weibull'
export type DiscreteDistType =
  | 'bernoulli'
  | 'binomial'
  | 'poisson'
  | 'geometric'
  | 'negative_binomial'
  | 'hypergeometric'
export type DistributionType = 'none' | ContinuousDistType | DiscreteDistType

const CONTINUOUS_DISTRIBUTIONS: ContinuousDistType[] = [
  'uniform',
  'exponential',
  'normal',
  'weibull',
]

const DISCRETE_DISTRIBUTIONS: DiscreteDistType[] = [
  'bernoulli',
  'binomial',
  'poisson',
  'geometric',
  'negative_binomial',
  'hypergeometric',
]

export interface GeneratorParams {
  method: GeneratorMethod
  seed: number
  a?: number
  c?: number
  m?: number
  digits?: number
  quantity: number
  alpha: number
  continuousDist?: ContinuousDistType
  discreteDist?: DiscreteDistType
  distParams?: {
    a?: number
    b?: number
    lambd?: number
    mean?: number
    stdDev?: number
    alpha?: number
    beta?: number
    p?: number
    n?: number
    r?: number
    N?: number
    K?: number
    n_sample?: number
    lambda?: number
  }
}

interface SidebarProps {
  onGenerate: (params: GeneratorParams) => void
  isLoading: boolean
}

export const Sidebar: React.FC<SidebarProps> = ({
  onGenerate,
  isLoading,
}) => {
  const [method, setMethod] = useState<GeneratorMethod>('lineal')
  const [seed, setSeed] = useState<string>('37')
  const [a, setA] = useState<string>('19')
  const [c, setC] = useState<string>('33')
  const [m, setM] = useState<string>('100')
  const [digits, setDigits] = useState<string>('4')
  const [quantity, setQuantity] = useState<string>('100')
  const [alpha, setAlpha] = useState<string>('0.05')

  // Estados para variable aleatoria (continua o discreta)
  const [dist, setDist] = useState<DistributionType>('none')
  const [uniformA, setUniformA] = useState<string>('0')
  const [uniformB, setUniformB] = useState<string>('10')
  const [expLambda, setExpLambda] = useState<string>('0.5')
  const [normMean, setNormMean] = useState<string>('0')
  const [normStd, setNormStd] = useState<string>('1')
  const [weiAlpha, setWeiAlpha] = useState<string>('1')
  const [weiBeta, setWeiBeta] = useState<string>('1.5')

  // Parámetros para distribuciones discretas
  const [bernP, setBernP] = useState<string>('0.5')
  const [binN, setBinN] = useState<string>('10')
  const [binP, setBinP] = useState<string>('0.5')
  const [poisLambda, setPoisLambda] = useState<string>('3')
  const [geoP, setGeoP] = useState<string>('0.3')
  const [nbR, setNbR] = useState<string>('5')
  const [nbP, setNbP] = useState<string>('0.5')
  const [hypN, setHypN] = useState<string>('100')
  const [hypK, setHypK] = useState<string>('50')
  const [hypSample, setHypSample] = useState<string>('10')

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault()
    const params: GeneratorParams = {
      method,
      seed: Number(seed),
      quantity: Number(quantity),
      alpha: Number(alpha),
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

    if (dist !== 'none') {
      params.distParams = {}

      if (CONTINUOUS_DISTRIBUTIONS.includes(dist as ContinuousDistType)) {
        params.continuousDist = dist as ContinuousDistType
        if (dist === 'uniform') {
          params.distParams.a = Number(uniformA)
          params.distParams.b = Number(uniformB)
        } else if (dist === 'exponential') {
          params.distParams.lambd = Number(expLambda)
        } else if (dist === 'normal') {
          params.distParams.mean = Number(normMean)
          params.distParams.stdDev = Number(normStd)
        } else if (dist === 'weibull') {
          params.distParams.alpha = Number(weiAlpha)
          params.distParams.beta = Number(weiBeta)
        }
      } else if (DISCRETE_DISTRIBUTIONS.includes(dist as DiscreteDistType)) {
        params.discreteDist = dist as DiscreteDistType
        if (dist === 'bernoulli') {
          params.distParams.p = Number(bernP)
        } else if (dist === 'binomial') {
          params.distParams.n = Number(binN)
          params.distParams.p = Number(binP)
        } else if (dist === 'poisson') {
          params.distParams.lambda = Number(poisLambda)
        } else if (dist === 'geometric') {
          params.distParams.p = Number(geoP)
        } else if (dist === 'negative_binomial') {
          params.distParams.r = Number(nbR)
          params.distParams.p = Number(nbP)
        } else if (dist === 'hypergeometric') {
          params.distParams.N = Number(hypN)
          params.distParams.K = Number(hypK)
          params.distParams.n_sample = Number(hypSample)
        }
      }
    }

    onGenerate(params)
  }

  return (
    <aside className="w-80 border-r border-slate-800 bg-[#171F33]/40 backdrop-blur-md flex flex-col h-[calc(100vh-4rem)] sticky top-16 scrollbar-none">
      {/* Algorithm Config Section */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-none">
        <div className="flex items-center gap-2 px-3">
          <Settings2 className="w-4 h-4 text-primary" />
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-widest font-label">Algoritmo Base</h3>
        </div>

        <form onSubmit={handleGenerate} className="space-y-4 px-3">
          {/* Method Select */}
          <div className="space-y-1.5">
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Método Pseudoaleatorio</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value as GeneratorMethod)}
              className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors cursor-pointer"
            >
              <option value="lineal">Congruencial Lineal / Mixto (LCG)</option>
              <option value="multiplicativo">Congruencia Multiplicativa (MCG)</option>
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
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Constante c (Incremento)</label>
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

          {/* Alpha / Significance Level */}
          <div className="space-y-1.5">
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Nivel de Significancia (α)</label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              max="0.99"
              value={alpha}
              onChange={(e) => setAlpha(e.target.value)}
              className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary transition-colors"
              required
            />
          </div>

          {/* Random Variable Section (Continuous + Discrete) */}
          <div className="pt-2 border-t border-slate-800 space-y-3">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" />
              <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-widest font-label">Variable Aleatoria</h3>
            </div>

            <div className="space-y-1.5">
              <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider font-label">Distribución Objetivo</label>
              <select
                value={dist}
                onChange={(e) => setDist(e.target.value as DistributionType)}
                className="w-full bg-[#0F172A] border border-slate-800 rounded-none px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500 transition-colors cursor-pointer"
              >
                <option value="none">Ninguna (U[0,1] puro)</option>
                <option value="uniform">Uniforme Continua U(A, B)</option>
                <option value="exponential">Exponencial (λ)</option>
                <option value="normal">Normal (μ, σ)</option>
                <option value="weibull">Weibull (α, β)</option>
                <option disabled className="bg-slate-800 text-slate-500 font-label">
                  ──── Variable Discreta ────
                </option>
                <option value="bernoulli">Bernoulli (p)</option>
                <option value="binomial">Binomial (n, p)</option>
                <option value="poisson">Poisson (λ)</option>
                <option value="geometric">Geométrica (p)</option>
                <option value="negative_binomial">Binomial Negativa (r, p)</option>
                <option value="hypergeometric">Hipergeométrica (N, K, n)</option>
              </select>
            </div>

            {/* Continuous Parameters */}
            {dist === 'uniform' && (
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Límite A</label>
                  <input
                    type="number"
                    step="any"
                    value={uniformA}
                    onChange={(e) => setUniformA(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Límite B</label>
                  <input
                    type="number"
                    step="any"
                    value={uniformB}
                    onChange={(e) => setUniformB(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}

            {dist === 'exponential' && (
              <div className="space-y-1 pt-1">
                <label className="block text-[10px] text-slate-400 font-label uppercase">Tasa Lambda (λ)</label>
                <input
                  type="number"
                  step="any"
                  min="0.0001"
                  value={expLambda}
                  onChange={(e) => setExpLambda(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>
            )}

            {dist === 'normal' && (
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Media (μ)</label>
                  <input
                    type="number"
                    step="any"
                    value={normMean}
                    onChange={(e) => setNormMean(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Desviación (σ)</label>
                  <input
                    type="number"
                    step="any"
                    min="0.0001"
                    value={normStd}
                    onChange={(e) => setNormStd(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}

            {dist === 'weibull' && (
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Escala (α)</label>
                  <input
                    type="number"
                    step="any"
                    min="0.0001"
                    value={weiAlpha}
                    onChange={(e) => setWeiAlpha(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Forma (β)</label>
                  <input
                    type="number"
                    step="any"
                    min="0.0001"
                    value={weiBeta}
                    onChange={(e) => setWeiBeta(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}

            {/* Discrete Parameters */}
            {dist === 'bernoulli' && (
              <div className="space-y-1 pt-1">
                <label className="block text-[10px] text-slate-400 font-label uppercase">Probabilidad de Éxito (p)</label>
                <input
                  type="number"
                  step="any"
                  min="0"
                  max="1"
                  value={bernP}
                  onChange={(e) => setBernP(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>
            )}

            {dist === 'binomial' && (
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Ensayos (n)</label>
                  <input
                    type="number"
                    min="1"
                    value={binN}
                    onChange={(e) => setBinN(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Probabilidad (p)</label>
                  <input
                    type="number"
                    step="any"
                    min="0"
                    max="1"
                    value={binP}
                    onChange={(e) => setBinP(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}

            {dist === 'poisson' && (
              <div className="space-y-1 pt-1">
                <label className="block text-[10px] text-slate-400 font-label uppercase">Lambda (λ)</label>
                <input
                  type="number"
                  step="any"
                  min="0.0001"
                  value={poisLambda}
                  onChange={(e) => setPoisLambda(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>
            )}

            {dist === 'geometric' && (
              <div className="space-y-1 pt-1">
                <label className="block text-[10px] text-slate-400 font-label uppercase">Probabilidad de Éxito (p)</label>
                <input
                  type="number"
                  step="any"
                  min="0.0001"
                  max="1"
                  value={geoP}
                  onChange={(e) => setGeoP(e.target.value)}
                  className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>
            )}

            {dist === 'negative_binomial' && (
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Éxitos (r)</label>
                  <input
                    type="number"
                    min="1"
                    value={nbR}
                    onChange={(e) => setNbR(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Probabilidad (p)</label>
                  <input
                    type="number"
                    step="any"
                    min="0.0001"
                    max="1"
                    value={nbP}
                    onChange={(e) => setNbP(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}

            {dist === 'hypergeometric' && (
              <div className="space-y-3 pt-1">
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <label className="block text-[10px] text-slate-400 font-label uppercase">Población (N)</label>
                    <input
                      type="number"
                      min="1"
                      value={hypN}
                      onChange={(e) => setHypN(e.target.value)}
                      className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                      required
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="block text-[10px] text-slate-400 font-label uppercase">Éxitos (K)</label>
                    <input
                      type="number"
                      min="0"
                      value={hypK}
                      onChange={(e) => setHypK(e.target.value)}
                      className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                      required
                    />
                  </div>
                </div>
                <div className="space-y-1">
                  <label className="block text-[10px] text-slate-400 font-label uppercase">Muestra (n)</label>
                  <input
                    type="number"
                    min="0"
                    value={hypSample}
                    onChange={(e) => setHypSample(e.target.value)}
                    className="w-full bg-[#0F172A] border border-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-primary to-tertiary hover:opacity-90 disabled:opacity-50 text-neutral font-bold py-2.5 px-4 rounded-xl shadow-lg shadow-primary/10 transition-all duration-200 active:scale-[0.98] cursor-pointer disabled:cursor-not-allowed flex items-center justify-center gap-2 text-xs"
          >
            <Calculator className="w-3.5 h-3.5" />
            {isLoading ? 'Generando...' : 'Generar Simulación'}
          </button>
        </form>
      </div>
    </aside>
  )
}
