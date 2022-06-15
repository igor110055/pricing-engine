import asyncio
import asyncclick as click
from pricing_engine.engine import PBDEngine
from pricing_engine.utils.stack import LockStack
from pricing_engine.utils.binance import binance_pbd_ws


@click.command()
@click.option("--topic", "-t", default="BTC_USDT", help="Topic to publish to")
async def main(topic):
    stack = LockStack()
    engine = PBDEngine(stack, topic)

    binance_symbol = "".join(filter(str.isalnum, topic)).lower()
    # TEMP: just for demo
    binance_busd = "".join(filter(str.isalnum, topic)).lower().replace("usdt", "busd")

    await asyncio.gather(
        engine.run(),
        binance_pbd_ws(stack, binance_symbol),
        binance_pbd_ws(stack, binance_busd),
        # * Add other provider websockets here, or create a class to control it later
    )


if __name__ == "__main__":
    try:
        main(_anyio_backend="asyncio")
    except KeyboardInterrupt:
        print("[Stopped by Ctrl+C]")
