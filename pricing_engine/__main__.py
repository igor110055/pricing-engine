import asyncio
import asyncclick as click
from pricing_engine.engine import PBDEngine
from pricing_engine.utils.producer import create_ck_producer
from pricing_engine.utils.binance import binance_pbd_ws
from pricing_engine.utils.stack import LockStack


@click.command()
@click.option("--topic", "-t", default="BTC_USDT", help="Topic to publish to")
async def main(topic):
    loop = asyncio.get_event_loop()
    producer = create_ck_producer(loop)

    binance_symbol = "".join(filter(str.isalnum, topic)).lower()
    binance_busd = "".join(filter(str.isalnum, topic)).lower().replace("usdt", "busd")

    stack = LockStack()
    engine = PBDEngine(producer, stack, topic)

    await producer.start()
    try:
        await asyncio.gather(
            engine.run(),
            binance_pbd_ws(stack, binance_symbol),
            binance_pbd_ws(stack, binance_busd),
        )
    finally:
        await producer.stop()


if __name__ == "__main__":
    try:
        main(_anyio_backend="asyncio")
    except KeyboardInterrupt:
        print("[Stopped by Ctrl+C]")
