class SimuStatError(Exception):
    """Excepción base para el dominio."""
    pass

class GeneratorValidationError(SimuStatError):
    """Error en validación de parámetros de generadores."""
    pass

class StatisticalTestError(SimuStatError):
    """Error en pruebas estadísticas."""
    pass

class StatsCalculationError(SimuStatError):
    """Error en cálculo de estadísticos."""
    pass