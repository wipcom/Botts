from app.models import MultiTimeframeAnalysis, ProbabilityResult, SignalSide


class TradeProbabilityEngine:
    """Scoring institucional configurable por features SMC."""

    def score(
        self,
        analysis: MultiTimeframeAnalysis,
        side: SignalSide,
    ) -> ProbabilityResult:
        score = 0
        reasons: list[str] = []
        smc = analysis.smc

        # Alineación de tendencia vs dirección propuesta.
        if analysis.bias.value == "BULLISH" and side == SignalSide.buy:
            score += 20
            reasons.append("Trend alignment +20")
        elif analysis.bias.value == "BEARISH" and side == SignalSide.sell:
            score += 20
            reasons.append("Trend alignment +20")

        if smc.liquidity_sweep:
            score += 20
            reasons.append("Liquidity sweep +20")
        if smc.bos:
            score += 15
            reasons.append("BOS +15")
        if smc.order_block_touch:
            score += 15
            reasons.append("Order block +15")
        if smc.fvg_entry:
            score += 15
            reasons.append("FVG entry +15")
        if smc.liquidity_target:
            score += 15
            reasons.append("Liquidity target +15")

        if analysis.bias.value == "RANGING":
            score -= 10
            reasons.append("Ranging penalty -10")

        score = max(0, min(score, 100))
        return ProbabilityResult(score=score, probability=score, reasons=reasons)
