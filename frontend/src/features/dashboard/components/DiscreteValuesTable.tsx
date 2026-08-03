import React, { useState } from 'react'
import { Table, Search } from 'lucide-react'

interface DiscreteValuesTableProps {
  numbers: number[]
  discreteValues: number[]
}

export const DiscreteValuesTable: React.FC<DiscreteValuesTableProps> = ({
  numbers,
  discreteValues,
}) => {
  const [filter, setFilter] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const pageSize = 50

  const combinedData = discreteValues.map((val, idx) => ({
    index: idx + 1,
    uVal: numbers[idx] !== undefined ? numbers[idx].toFixed(6) : '-',
    xVal: val,
  }))

  const filteredData = combinedData.filter(
    (item) =>
      item.index.toString().includes(filter) ||
      item.xVal.toString().includes(filter) ||
      item.uVal.includes(filter)
  )

  const totalPages = Math.ceil(filteredData.length / pageSize) || 1
  const paginatedData = filteredData.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  )

  return (
    <div className="bg-[#171F33]/60 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-violet-500/10 rounded-xl border border-violet-500/20 text-violet-400">
            <Table className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white font-headline">Variables Aleatorias Discretas Generadas</h3>
            <p className="text-xs text-slate-400">
              Mostrando {filteredData.length} de {discreteValues.length} números generados (X_i)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Buscar valor o índice..."
              value={filter}
              onChange={(e) => {
                setFilter(e.target.value)
                setCurrentPage(1)
              }}
              className="bg-[#0F172A] border border-slate-800 text-slate-200 text-xs rounded-xl pl-9 pr-3 py-2 focus:outline-none focus:border-violet-500 w-48"
            />
          </div>
        </div>
      </div>

      {/* Tabla con scroll interno */}
      <div className="overflow-x-auto max-h-96 rounded-xl border border-slate-800 bg-[#0F172A]/80 scrollbar-none">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-[#1E293B] text-slate-400 font-label uppercase sticky top-0 z-10">
            <tr>
              <th className="py-3 px-4"># (i)</th>
              <th className="py-3 px-4">U_i (Uniforme Base)</th>
              <th className="py-3 px-4 text-violet-400">X_i (Variable Discreta)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 font-mono">
            {paginatedData.length > 0 ? (
              paginatedData.map((row) => (
                <tr key={row.index} className="hover:bg-slate-800/50 transition-colors">
                  <td className="py-2.5 px-4 text-slate-500">{row.index}</td>
                  <td className="py-2.5 px-4 text-slate-300">{row.uVal}</td>
                  <td className="py-2.5 px-4 text-violet-400 font-bold">{row.xVal}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="py-6 text-center text-slate-500 font-body">
                  No se encontraron datos que coincidan con la búsqueda.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Paginación */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-2 text-xs font-label">
          <span className="text-slate-400">
            Página {currentPage} de {totalPages}
          </span>
          <div className="flex items-center gap-2">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-3 py-1 bg-[#0F172A] border border-slate-800 text-slate-300 rounded disabled:opacity-40 cursor-pointer"
            >
              Anterior
            </button>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-3 py-1 bg-[#0F172A] border border-slate-800 text-slate-300 rounded disabled:opacity-40 cursor-pointer"
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
