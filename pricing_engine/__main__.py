import asyncio
from pricing_engine.engine import PBDEngine
from pricing_engine.producer import Producer, load_ck_config

# LATER: turn this into cli?

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    configs = load_ck_config()

    producer = Producer(configs)

    # TODO: Use asyncio queue to collect bidask from different platform
    # TODO: sent to kafka in collector instead

    engine = PBDEngine(producer, 'ethusdt')

    try:
        loop.run_until_complete(engine.start())
    except KeyboardInterrupt:
        print('[Stopped by Ctrl+C]')
    finally:
        # OPTIONAL: use producer.flush() to wait for outstanding message delivery
        producer.close()
