import uuid

from app.models import RiskPlan, SignalSide


class BitunixExecutionEngine:
    """Adapter Bitunix.

    Actualmente simula ejecución y retorna un ID local.
    Sustituir por firma HMAC y endpoints reales de Bitunix.
    """

    def execute_trade(self, symbol: str, side: SignalSide, plan: RiskPlan) -> str:
        _ = (symbol, side, plan)
        return f"SIM-{uuid.uuid4().hex[:12]}"
