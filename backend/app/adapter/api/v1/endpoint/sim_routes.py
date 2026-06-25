# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException, status
from app.adapter.api.schema import SimulationRequest, SimulationResponse
from app.services.simulation_service import SimulationService
from app.domain.generators import GeneratorValidationError

router = APIRouter()


@router.post(
    "/generate-sequence",
    response_model=SimulationResponse,
    status_code=status.HTTP_200_OK,
    summary="Genera una secuencia de números pseudoaleatorios y aplica validaciones estadísticas",
    description="Genera una secuencia usando LCG, MCG o Mid-Square y le aplica las pruebas de media, varianza y Kolmogorov-Smirnov."
)
def generate_sequence(request: SimulationRequest) -> SimulationResponse:
    try:
        return SimulationService.run_simulation(request)
    except GeneratorValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado al procesar la simulación: {str(e)}"
        )
