import React from 'react'
import { Grafica } from './Grafica'
import { DistribucionUniforme } from './DistribucionUniforme'
import { TestMedia } from './TestMedia'
import { TestVarianza } from './TestVarianza'
import { TestKS } from './TestKS'
import { TestRacha } from './TestRacha'
import type { SimulationData } from './types'

interface DashboardProps {
  data: SimulationData | null
}

export const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  return (
    <div className="space-y-6">
      {/* Fila superior: Gráfica + Distribución */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Grafica numbers={data?.numbers ?? []} />
        </div>
        <div>
          <DistribucionUniforme numbers={data?.numbers ?? []} />
        </div>
      </div>

      {/* Fila inferior: Tests estadísticos */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <TestMedia result={data?.mean_test ?? null} />
        <TestVarianza result={data?.variance_test ?? null} />
        <TestKS result={data?.ks_test ?? null} />
        <TestRacha result={data?.streak_test ?? null} />
      </div>
    </div>
  )
}

