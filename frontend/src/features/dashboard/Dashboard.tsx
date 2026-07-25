import React from 'react'
import { Grafica } from './Grafica'
import { DistribucionUniforme } from './DistribucionUniforme'
import { TestMedia } from './TestMedia'
import { TestVarianza } from './TestVarianza'
import { TestKS } from './TestKS'
import { TestRacha } from './TestRacha'
import { ContinuousValuesTable } from './components/ContinuousValuesTable'
import type { SimulationData } from './types'

interface DashboardProps {
  data: SimulationData | null
}

export const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const hasContinuous = Boolean(data?.continuous_values && data.continuous_values.length > 0)

  return (
    <div className="space-y-8">
      {/* Muestra únicamente la tabla de Variables Aleatorias Continuas Generadas */}
      {hasContinuous && data?.continuous_values && (
        <div className="space-y-6">
          <ContinuousValuesTable
            numbers={data.numbers}
            continuousValues={data.continuous_values}
          />
        </div>
      )}

      {/* Sección del Generador Pseudoaleatorio Base U(0,1) y Pruebas Estadísticas */}
      <div className="pt-4 border-t border-slate-800 space-y-6">
        <div>
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider font-label mb-3">
            Generador Pseudoaleatorio Base U(0,1) y Pruebas Estadísticas
          </h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Grafica numbers={data?.numbers ?? []} />
            </div>
            <div>
              <DistribucionUniforme numbers={data?.numbers ?? []} />
            </div>
          </div>
        </div>

        {/* Pruebas estadísticas U(0,1) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <TestMedia result={data?.mean_test ?? null} />
          <TestVarianza result={data?.variance_test ?? null} />
          <TestKS result={data?.ks_test ?? null} />
          <TestRacha result={data?.streak_test ?? null} />
        </div>
      </div>
    </div>
  )
}
