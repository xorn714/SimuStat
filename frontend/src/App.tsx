import { useState, useCallback } from 'react'
import { Navbar } from './components/layout/navbar'
import { Sidebar } from './components/layout/sidebar'
import { Dashboard } from './features/dashboard/Dashboard'
import { generateSequence } from './services/api'
import type { GeneratorParams } from './components/layout/sidebar'
import type { SimulationData } from './features/dashboard/types'

function App() {
  const [lastParams, setLastParams] = useState<GeneratorParams | null>(null)
  const [simulationData, setSimulationData] = useState<SimulationData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = useCallback(async (params: GeneratorParams) => {
    setLastParams(params)
    setError(null)
    setIsLoading(true)
    setSimulationData(null)

    try {
      const data = await generateSequence(params)
      setSimulationData(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setIsLoading(false)
    }
  }, [])

  return (
    <div className="min-h-screen bg-neutral text-slate-100 flex flex-col font-body">
      {/* Barra de navegación superior */}
      <Navbar />

      {/* Contenedor principal con sidebar y contenido */}
      <div className="flex flex-1">
        {/* Barra lateral */}
        <Sidebar
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />

        {/* Panel de contenido */}
        <main className="flex-1 p-8 overflow-y-auto">
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-black text-white font-headline">Dashboard</h1>
              <p className="text-slate-400">Panel principal de SimuStat — resultados de la simulación activa.</p>
            </div>

            {lastParams && (
              <div className="p-4 rounded-xl border border-primary/20 bg-primary/5">
                <h3 className="text-sm font-semibold text-primary font-label uppercase tracking-wider mb-2">Configuración Activa</h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-label text-slate-300">
                  <div><span className="text-slate-500">Método:</span> {lastParams.method}</div>
                  <div><span className="text-slate-500">Semilla X₀:</span> {lastParams.seed}</div>
                  <div><span className="text-slate-500">Cantidad N:</span> {lastParams.quantity}</div>
                  <div><span className="text-slate-500">α:</span> {lastParams.alpha}</div>
                  {lastParams.a !== undefined && <div><span className="text-slate-500">Constante a:</span> {lastParams.a}</div>}
                  {lastParams.c !== undefined && <div><span className="text-slate-500">Constante c:</span> {lastParams.c}</div>}
                  {lastParams.m !== undefined && <div><span className="text-slate-500">Módulo m:</span> {lastParams.m}</div>}
                  {lastParams.digits !== undefined && <div><span className="text-slate-500">Dígitos:</span> {lastParams.digits}</div>}
                  {lastParams.continuousDist && <div><span className="text-slate-500">Dist. Continua:</span> {lastParams.continuousDist}</div>}
                  {lastParams.discreteDist && <div><span className="text-slate-500">Dist. Discreta:</span> {lastParams.discreteDist}</div>}
                </div>
              </div>
            )}

            {isLoading && (
              <div className="flex items-center justify-center py-12">
                <div className="flex flex-col items-center gap-4">
                  <div className="w-10 h-10 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
                  <p className="text-sm text-slate-400">Generando simulación...</p>
                </div>
              </div>
            )}

            {error && (
              <div className="p-4 rounded-xl border border-red-500/40 bg-red-500/10">
                <p className="text-sm text-red-400 font-semibold">Error: {error}</p>
              </div>
            )}

            {!isLoading && simulationData && (
              <Dashboard
                data={simulationData}
                distName={lastParams?.continuousDist || lastParams?.discreteDist}
                distParams={lastParams?.distParams}
              />
            )}

            {!isLoading && !simulationData && !error && (
              <div className="flex flex-col items-center justify-center py-20 border border-dashed border-slate-800 rounded-2xl bg-[#171F33]/20">
                <p className="text-slate-400 text-sm mb-1">No se han generado datos todavía.</p>
                <p className="text-slate-500 text-xs">Configure el algoritmo a la izquierda y presione "Generar" para ver los resultados.</p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
