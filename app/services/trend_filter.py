from app.models import MarketBias


def infer_market_bias(timeframe_trends: dict[str, str]) -> str:
    """Determina bias institucional a partir del contexto HTF/MTF."""

    bullish_votes = sum(1 for _, v in timeframe_trends.items() if v == "bullish")
    bearish_votes = sum(1 for _, v in timeframe_trends.items() if v == "bearish")

    if bullish_votes >= 2 and bearish_votes == 0:
        return MarketBias.BULLISH.value
    if bearish_votes >= 2 and bullish_votes == 0:
        return MarketBias.BEARISH.value
    return MarketBias.RANGING.value
