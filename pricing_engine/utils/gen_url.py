
# Constant Formats
BINANCE_WS = 'wss://stream.binance.com:9443/ws'
BINANCE_PBT_WS = BINANCE_WS+'/{symbol}@depth{levels}'
MS_TICKER = '@100ms'


def gen_binance_pbd_ws_url(symbol: str, levels: int = 5, ms: bool = False):
    if levels not in [5, 10, 20]:
        raise ValueError('Level must be 5, 10 or 20')

    base_url = BINANCE_PBT_WS.format(symbol=symbol, levels=levels)
    return ''.join([base_url, MS_TICKER]) if ms else base_url
