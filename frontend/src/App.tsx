import { useState } from 'react'
import { Navbar } from './components/layout/navbar'
import type { TabType } from './components/layout/navbar'

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard')

  return (
    <div className="min-h-screen bg-neutral text-slate-100 flex flex-col font-body">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {activeTab === 'dashboard' && (
          <div className="space-y-4">
            <h1 className="text-3xl font-black text-white font-headline">Dashboard</h1>
            <p className="text-slate-400">Panel principal de SimuStat. Bienvenido.</p>
          </div>
        )}

        {activeTab === 'modelos' && (
          <div className="space-y-4">
            <h1 className="text-3xl font-black text-white font-headline">Modelos</h1>
            <p className="text-slate-400">Configuración y generación de modelos pseudoaleatorios.</p>
          </div>
        )}

        {activeTab === 'analiticas' && (
          <div className="space-y-4">
            <h1 className="text-3xl font-black text-white font-headline">Analíticas</h1>
            <p className="text-slate-400">Pruebas estadísticas y validación de datos.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
