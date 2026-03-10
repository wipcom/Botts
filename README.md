# Plataforma de Autotrading SMC + TradingView + Bitunix

Arquitectura inicial profesional para recibir alertas de TradingView, validarlas con análisis institucional (Smart Money Concepts), puntuar probabilidad y ejecutar operaciones en Bitunix con gestión de riesgo.

## Objetivo del sistema

Este proyecto implementa una base modular para:

1. Recibir alertas webhook de TradingView.
2. Analizar contexto multi-timeframe (1D, 4H, 1H, 15M).
3. Validar condiciones SMC (BOS, MSS, sweep, OB, FVG, etc.).
4. Calcular probabilidad de trade y filtrar señales débiles.
5. Aplicar riesgo institucional (1%-2% por operación, R:R >= 1:2).
6. Ejecutar órdenes en Bitunix (adapter listo para integrar API real).
7. Exponer un dashboard en tiempo real (estado de mercado y señales).

## Stack

- Backend: FastAPI
- Motor de análisis: Python
- DB objetivo: PostgreSQL (pendiente integración en esta base)
- Dashboard objetivo: React/NextJS (la API ya expone endpoints para consumir)

## Estructura

```text
app/
  main.py
  models.py
  core/
    config.py
  services/
    signal_processor.py
    market_analysis.py
    smc_engine.py
    trend_filter.py
    probability_engine.py
    risk_management.py
    execution_bitunix.py
    dashboard_state.py
tests/
  test_pipeline.py
```

## Flujo

TradingView Alert -> Webhook API -> Signal Processor -> Market Analysis -> SMC Validation -> Trend Filter -> Probability Engine -> Risk Management -> Bitunix Execution -> Dashboard State

## Reglas clave implementadas

- `trade_probability >= 65` para ejecutar.
- Si bias es `BULLISH`, solo BUY.
- Si bias es `BEARISH`, solo SELL.
- Si bias es `RANGING`, requiere confluencia más estricta (score mínimo +10 extra).
- R:R mínimo 1:2.
- Riesgo por trade configurable (`1%` por defecto).

## Ejecutar en local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Endpoint principal

- `POST /webhook/tradingview`

Ejemplo payload:

```json
{
  "symbol": "BTCUSDT",
  "signal": "buy",
  "price": 68170,
  "timeframe": "15m",
  "strategy": "SMC_ENTRY"
}
```

### Dashboard API

- `GET /dashboard/state`

## Integración real Bitunix

La clase `BitunixExecutionEngine` tiene un método `execute_trade` preparado para reemplazar la simulación por llamadas reales firmadas con API Key/Secret.

## Próximos pasos recomendados

1. Integrar feed OHLCV real (WebSocket + REST) para BTC, ETH, SOL, XRP.
2. Persistir análisis/señales/trades en PostgreSQL.
3. Conectar frontend NextJS para visualización institucional (zonas liquidez, sweeps, OB/FVG).
4. Sustituir lógica heurística SMC por detección cuantitativa robusta.
5. Añadir backtesting y evaluación walk-forward.
