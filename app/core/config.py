from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Configuración central del sistema de trading."""

    min_probability: int = Field(default=65, ge=0, le=100)
    risk_per_trade: float = Field(default=0.01, ge=0.0, le=0.02)
    min_rr: float = Field(default=2.0, ge=1.0)


settings = Settings()
