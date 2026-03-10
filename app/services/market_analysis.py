from app.models import MarketBias, MultiTimeframeAnalysis
from app.services.smc_engine import detect_smc_features
from app.services.trend_filter import infer_market_bias


class MarketAnalysisEngine:
    """Motor que consolida análisis MTF + detección SMC."""

    def analyze(self, symbol: str, price: float) -> MultiTimeframeAnalysis:
        # En producción, este bloque debe consumir OHLCV real de 1D/4H/1H/15M.
        timeframe_trends = {
            "1D": "bullish" if price % 2 else "bearish",
            "4H": "bullish",
            "1H": "bullish" if price % 3 else "ranging",
            "15M": "pullback",
        }

        bias = infer_market_bias(timeframe_trends)
        smc = detect_smc_features(symbol=symbol, price=price)

        return MultiTimeframeAnalysis(
            symbol=symbol,
            timeframe_trends=timeframe_trends,
            bias=MarketBias(bias),
            smc=smc,
        )
