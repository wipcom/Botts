from app.core.config import settings
from app.models import SignalSide, TradeDecision, TradingViewAlert
from app.services.execution_bitunix import BitunixExecutionEngine
from app.services.market_analysis import MarketAnalysisEngine
from app.services.probability_engine import TradeProbabilityEngine
from app.services.risk_management import RiskManagementEngine


class SignalProcessor:
    """Orquestador principal: valida, puntúa, gestiona riesgo y ejecuta."""

    def __init__(self) -> None:
        self.market_engine = MarketAnalysisEngine()
        self.probability_engine = TradeProbabilityEngine()
        self.risk_engine = RiskManagementEngine()
        self.execution_engine = BitunixExecutionEngine()

    def process(self, alert: TradingViewAlert) -> TradeDecision:
        analysis = self.market_engine.analyze(symbol=alert.symbol, price=alert.price)

        # Filtro de tendencia institucional.
        if analysis.bias.value == "BULLISH" and alert.signal != SignalSide.buy:
            probability = self.probability_engine.score(analysis, alert.signal)
            return TradeDecision(
                accepted=False,
                reason="Señal rechazada: bias BULLISH solo permite BUY.",
                analysis=analysis,
                probability=probability,
            )

        if analysis.bias.value == "BEARISH" and alert.signal != SignalSide.sell:
            probability = self.probability_engine.score(analysis, alert.signal)
            return TradeDecision(
                accepted=False,
                reason="Señal rechazada: bias BEARISH solo permite SELL.",
                analysis=analysis,
                probability=probability,
            )

        probability = self.probability_engine.score(analysis, alert.signal)

        min_probability = settings.min_probability + (10 if analysis.bias.value == "RANGING" else 0)
        if probability.probability < min_probability:
            return TradeDecision(
                accepted=False,
                reason=f"Probabilidad insuficiente ({probability.probability} < {min_probability}).",
                analysis=analysis,
                probability=probability,
            )

        plan = self.risk_engine.build_plan(side=alert.signal, entry=alert.price)
        if plan.rr < settings.min_rr:
            return TradeDecision(
                accepted=False,
                reason=f"R:R insuficiente ({plan.rr:.2f} < {settings.min_rr}).",
                analysis=analysis,
                probability=probability,
                risk_plan=plan,
            )

        execution_id = self.execution_engine.execute_trade(alert.symbol, alert.signal, plan)
        return TradeDecision(
            accepted=True,
            reason="Trade aprobado y ejecutado.",
            analysis=analysis,
            probability=probability,
            risk_plan=plan,
            execution_id=execution_id,
        )
