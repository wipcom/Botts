from app.models import SMCFeatures


# Nota: heurística placeholder. Debe sustituirse por detección real SMC sobre velas/estructura.
def detect_smc_features(symbol: str, price: float) -> SMCFeatures:
    base = int(price)
    return SMCFeatures(
        liquidity_sweep=base % 2 == 0,
        bos=base % 3 != 0,
        mss=base % 5 != 0,
        order_block_touch=base % 7 < 4,
        fvg_entry=base % 11 < 6,
        confluence_zone=base % 13 < 8,
        liquidity_target=base % 17 < 10,
    )
