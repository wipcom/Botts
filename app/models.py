from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SignalSide(str, Enum):
    buy = "buy"
    sell = "sell"


class MarketBias(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    RANGING = "RANGING"


class TradingViewAlert(BaseModel):
    symbol: str
    signal: SignalSide
    price: float
    timeframe: str
    strategy: str


class SMCFeatures(BaseModel):
    liquidity_sweep: bool = False
    bos: bool = False
    mss: bool = False
    order_block_touch: bool = False
    fvg_entry: bool = False
    confluence_zone: bool = False
    liquidity_target: bool = False


class MultiTimeframeAnalysis(BaseModel):
    symbol: str
    timeframe_trends: Dict[str, str]
    bias: MarketBias
    smc: SMCFeatures


class ProbabilityResult(BaseModel):
    score: int = Field(ge=0, le=100)
    probability: int = Field(ge=0, le=100)
    reasons: List[str]


class RiskPlan(BaseModel):
    entry: float
    stop_loss: float
    tp1: float
    tp2: float
    tp3: float
    rr: float
    position_size: float


class TradeDecision(BaseModel):
    accepted: bool
    reason: str
    analysis: MultiTimeframeAnalysis
    probability: ProbabilityResult
    risk_plan: Optional[RiskPlan] = None
    execution_id: Optional[str] = None
