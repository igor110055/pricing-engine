import asyncio
import asyncclick as click
from pricing_engine.engine import PBDEngine
from pricing_engine.utils.producer import create_ck_producer
from pricing_engine.utils.binance import binance_pbd_ws
from pricing_engine.utils.stack import LockStack


@click.command()
@click.option('--topic', '-t', default='BTC_USDT', help='Topic to publish to')
async def main(topic):
    loop = asyncio.get_event_loop()
    producer = create_ck_producer(loop)

    binance_symbol = ''.join(filter(str.isalnum, topic)).lower()

    stack = LockStack()
    engine = PBDEngine(producer, stack, topic)

    # FIXME: async does not catch ctrl+c
    await producer.start()
    try:
        await asyncio.gather(
            engine.run(),
            binance_pbd_ws(stack, binance_symbol),
        )
    except KeyboardInterrupt:
        print('[Stopped by Ctrl+C]')
    finally:
        await producer.stop()


if __name__ == '__main__':
    main(_anyio_backend="asyncio")
