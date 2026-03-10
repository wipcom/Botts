from fastapi import FastAPI

from app.models import TradingViewAlert
from app.services.dashboard_state import DashboardState
from app.services.signal_processor import SignalProcessor

app = FastAPI(title="SMC AutoTrading Platform", version="0.1.0")
processor = SignalProcessor()
dashboard_state = DashboardState()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/webhook/tradingview")
def tradingview_webhook(alert: TradingViewAlert) -> dict:
    decision = processor.process(alert)
    payload = {
        "symbol": alert.symbol,
        "signal": alert.signal.value,
        "accepted": decision.accepted,
        "reason": decision.reason,
        "bias": decision.analysis.bias.value,
        "probability": decision.probability.probability,
        "execution_id": decision.execution_id,
        "risk_plan": decision.risk_plan.model_dump() if decision.risk_plan else None,
    }
    dashboard_state.push(payload)
    return payload


@app.get("/dashboard/state")
def dashboard_snapshot() -> dict:
    return dashboard_state.snapshot()
