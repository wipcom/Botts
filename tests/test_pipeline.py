from app.models import SignalSide, TradingViewAlert
from app.services.signal_processor import SignalProcessor


def test_process_returns_decision_object_with_probability_bounds():
    processor = SignalProcessor()
    alert = TradingViewAlert(
        symbol="BTCUSDT",
        signal=SignalSide.buy,
        price=68170,
        timeframe="15m",
        strategy="SMC_ENTRY",
    )

    decision = processor.process(alert)

    assert 0 <= decision.probability.probability <= 100
    assert decision.reason


def test_if_trade_accepted_then_execution_and_risk_plan_exist():
    processor = SignalProcessor()
    alert = TradingViewAlert(
        symbol="ETHUSDT",
        signal=SignalSide.buy,
        price=70001,
        timeframe="15m",
        strategy="SMC_ENTRY",
    )

    decision = processor.process(alert)

    if decision.accepted:
        assert decision.execution_id is not None
        assert decision.risk_plan is not None
        assert decision.risk_plan.rr >= 2.0
