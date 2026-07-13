import type { SimulationData } from '../features/dashboard/types'
import type { GeneratorParams } from '../components/layout/sidebar'

const API_BASE_URL = 'http://localhost:8000/api/v1'

function mapMethod(method: string): string {
  switch (method) {
    case 'lineal':
      return 'lcg'
    case 'multiplicativo':
      return 'mcg'
    case 'cuadrados_medios':
      return 'mid_square'
    default:
      throw new Error(`Método desconocido: ${method}`)
  }
}

export async function generateSequence(
  params: GeneratorParams & { alpha: number }
): Promise<SimulationData> {
  const response = await fetch(`${API_BASE_URL}/generate-sequence`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      method: mapMethod(params.method),
      semilla: params.seed,
      a: params.a,
      c: params.c,
      m: params.m,
      n: params.quantity,
      digits: params.digits,
      alpha: params.alpha,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error de conexión con el servidor' }))
    throw new Error(error.detail || 'Error al generar la simulación')
  }

  return response.json()
}

export async function checkBackendStatus(): Promise<boolean> {
  try {
    const response = await fetch('http://localhost:8000/', { method: 'GET' })
    return response.ok
  } catch {
    return false
  }
}

