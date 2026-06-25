import { useState } from 'react'
import { Navbar } from './components/layout/navbar'
import { Sidebar } from './components/layout/sidebar'
import type { SidebarTabType, GeneratorParams } from './components/layout/sidebar'

function App() {
  const [activeSidebarTab, setActiveSidebarTab] = useState<SidebarTabType>('dashboard')
  const [lastParams, setLastParams] = useState<GeneratorParams | null>(null)

  const handleGenerate = (params: GeneratorParams) => {
    setLastParams(params)
    // Cambiar automáticamente a la vista de simulación para mostrar los resultados
    setActiveSidebarTab('simulacion')
    console.log('Parámetros generados:', params)
  }

  return (
    <div className="min-h-screen bg-neutral text-slate-100 flex flex-col font-body">
      {/* Barra de navegación superior */}
      <Navbar />

      {/* Contenedor principal con sidebar y contenido */}
      <div className="flex flex-1">
        {/* Barra lateral */}
        <Sidebar
          activeTab={activeSidebarTab}
          setActiveTab={setActiveSidebarTab}
          onGenerate={handleGenerate}
        />

        {/* Panel de contenido */}
        <main className="flex-1 p-8 overflow-y-auto">
          {activeSidebarTab === 'dashboard' && (
            <div className="space-y-4">
              <h1 className="text-3xl font-black text-white font-headline">Dashboard</h1>
              <p className="text-slate-400">Panel principal de SimuStat. Seleccione una opción en el menú lateral para comenzar.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                <div className="p-6 rounded-2xl border border-slate-800 bg-[#171F33]/20">
                  <h3 className="text-lg font-bold text-white font-headline mb-2">Generación rápida</h3>
                  <p className="text-sm text-slate-400">
                    Use el configurador de la barra lateral para definir los parámetros y generar números pseudoaleatorios al instante.
                  </p>
                </div>
                <div className="p-6 rounded-2xl border border-slate-800 bg-[#171F33]/20">
                  <h3 className="text-lg font-bold text-white font-headline mb-2">Validación Estadística</h3>
                  <p className="text-sm text-slate-400">
                    Someteremos los números a pruebas de Media, Varianza y Kolmogorov-Smirnov para validar su uniformidad.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeSidebarTab === 'simulacion' && (
            <div className="space-y-4">
              <h1 className="text-3xl font-black text-white font-headline">Simulación</h1>
              {lastParams ? (
                <div className="space-y-6">
                  <div className="p-4 rounded-xl border border-primary/20 bg-primary/5">
                    <h3 className="text-sm font-semibold text-primary font-label uppercase tracking-wider mb-2">Configuración Activa</h3>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-label text-slate-300">
                      <div><span className="text-slate-500">Método:</span> {lastParams.method}</div>
                      <div><span className="text-slate-500">Semilla X₀:</span> {lastParams.seed}</div>
                      <div><span className="text-slate-500">Cantidad N:</span> {lastParams.quantity}</div>
                      {lastParams.a !== undefined && <div><span className="text-slate-500">Constante a:</span> {lastParams.a}</div>}
                      {lastParams.c !== undefined && <div><span className="text-slate-500">Constante c:</span> {lastParams.c}</div>}
                      {lastParams.m !== undefined && <div><span className="text-slate-500">Módulo m:</span> {lastParams.m}</div>}
                      {lastParams.digits !== undefined && <div><span className="text-slate-500">Dígitos:</span> {lastParams.digits}</div>}
                    </div>
                  </div>
                  <p className="text-slate-400">Resultados y simulación listos para procesamiento backend...</p>
                </div>
              ) : (
                <p className="text-slate-400">No se han generado datos todavía. Configure el algoritmo a la izquierda y presione "Generar".</p>
              )}
            </div>
          )}

          {activeSidebarTab === 'historial' && (
            <div className="space-y-4">
              <h1 className="text-3xl font-black text-white font-headline">Historial</h1>
              <p className="text-slate-400">Lista de secuencias pseudoaleatorias generadas anteriormente.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
