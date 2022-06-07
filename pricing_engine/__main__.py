import asyncio
from pricing_engine.engine import main

# TEMP: env
WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5"

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(WS_URL))
    except KeyboardInterrupt:
        print('[Stopped by Ctrl+C]')
