import logging
import json
from websockets import connect
from websockets.exceptions import ConnectionClosed
from pricing_engine.utils.stack import LockStack


BINANCE_WS = "wss://stream.binance.com:9443/ws"
BINANCE_PBT_WS = BINANCE_WS + "/{symbol}@depth{levels}"
MS_TICKER = "@100ms"

logger = logging.getLogger(__name__)


def gen_binance_pbd_ws_url(symbol: str, levels: int = 5, ms: bool = False):
    if levels not in [5, 10, 20]:
        raise ValueError("Level must be 5, 10 or 20")

    base_url = BINANCE_PBT_WS.format(symbol=symbol, levels=levels)
    return "".join([base_url, MS_TICKER]) if ms else base_url


async def binance_pbd_ws(
    stack: LockStack,
    symbol: str,
    levels: int = 5,
    ms: bool = False,
):
    url = gen_binance_pbd_ws_url(symbol, levels, ms)

    async for websocket in connect(url):
        logger.info(f"Connected to {url}")
        try:
            async for message in websocket:
                data = json.loads(message)
                exchange_symbol = "%s-%s"%('binance', symbol)
                data["bids"] = [x+[exchange_symbol] for x in data["bids"]]
                data["asks"] = [x+[exchange_symbol] for x in data["asks"]]
                stack_data = {key: data[key] for key in ("bids", "asks")}
                await stack.append(stack_data)
        except ConnectionClosed:
            logger.warn(f"Disconnected from {url}, reconnecting...")
            continue
