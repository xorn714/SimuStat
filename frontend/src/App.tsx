import { useState } from 'react'
import { Beaker, Calculator, CheckCircle2, TrendingUp } from 'lucide-react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 selection:bg-purple-500 selection:text-white">
      {/* Header / Brand */}
      <div className="max-w-4xl w-full text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-400 text-sm font-medium mb-2 animate-pulse">
          <Beaker className="w-4 h-4" />
          Simuladores y Validación Estadística
        </div>
        <h1 className="text-5xl md:text-6xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-500 to-indigo-400">
          SimuStat
        </h1>
        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto">
          Generación y validación de variables aleatorias uniformes y discretas mediante
          Método de Composición, Inversión, Congruencial y Cuadrados Medios.
        </p>
      </div>

      {/* Main Grid Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl w-full mt-12">
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl hover:border-purple-500/50 transition-all duration-300 group">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-110 transition-transform">
            <Calculator className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Generadores Uniformes</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Implementación de algoritmos de <strong>Método Congruencial</strong> (Lineal y Multiplicativo) y <strong>Método de Cuadrados Medios</strong> para la generación de secuencias pseudoaleatorias.
          </p>
        </div>

        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl hover:border-indigo-500/50 transition-all duration-300 group">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Pruebas de Validación</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Validación de los conjuntos de números generados mediante tres pruebas estadísticas fundamentales:
            <strong>Prueba de Media</strong>, <strong>Prueba de Varianza</strong> y <strong>Prueba de Bondad de Ajuste Kolmogorov-Smirnov</strong>.
          </p>
        </div>

        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl hover:border-pink-500/50 transition-all duration-300 group md:col-span-2">
          <div className="w-12 h-12 rounded-xl bg-pink-500/10 border border-pink-500/30 flex items-center justify-center text-pink-400 mb-4 group-hover:scale-110 transition-transform">
            <TrendingUp className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Variables Discretas</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Simulación de variables aleatorias discretas a través de los métodos de <strong>Composición</strong> e <strong>Inversión</strong> para modelar escenarios probabilísticos complejos basados en distribuciones de probabilidad no uniformes.
          </p>
        </div>
      </div>

      {/* Connection Test / Status */}
      <div className="mt-12 flex flex-col items-center gap-4">
        <button
          onClick={() => setCount(count + 1)}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold shadow-lg shadow-purple-900/30 transition-all duration-200 active:scale-95"
        >
          Prueba React HMR: {count}
        </button>
        <span className="text-xs text-slate-500">
          Backend API: <code className="bg-slate-900 px-2 py-1 rounded text-purple-400 font-mono">http://localhost:8000/docs</code> (Swagger UI)
        </span>
      </div>
    </div>
  )
}

export default App
