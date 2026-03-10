from app.core.config import settings
from app.models import RiskPlan, SignalSide


class RiskManagementEngine:
    """Planifica SL/TP/size respetando riesgo institucional y R:R mínimo."""

    def build_plan(self, side: SignalSide, entry: float, equity_usdt: float = 10000.0) -> RiskPlan:
        # Distancia SL simplificada (0.5% del precio). Reemplazar por estructura real.
        sl_distance = entry * 0.005

        if side == SignalSide.buy:
            stop_loss = entry - sl_distance
            tp1 = entry + sl_distance * settings.min_rr
        else:
            stop_loss = entry + sl_distance
            tp1 = entry - sl_distance * settings.min_rr

        # Escalado de targets.
        tp2 = entry + (tp1 - entry) * 1.5
        tp3 = entry + (tp1 - entry) * 2.0

        # Riesgo monetario fijo por trade.
        risk_amount = equity_usdt * settings.risk_per_trade
        position_size = risk_amount / sl_distance

        rr = abs((tp1 - entry) / (entry - stop_loss)) if entry != stop_loss else settings.min_rr

        return RiskPlan(
            entry=entry,
            stop_loss=stop_loss,
            tp1=tp1,
            tp2=tp2,
            tp3=tp3,
            rr=rr,
            position_size=position_size,
        )
