import asyncio
import logging
import json
from typing import List
from itertools import chain
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from pricing_engine.utils.stack import LockStack


logger = logging.getLogger(__name__)


class PBDEngine:
    """Pricing engine implementation based on Partial Book Depth (PBD)."""

    def __init__(self, producer: AIOKafkaProducer, stack: LockStack, topic: str) -> None:
        self._producer = producer
        self._stack = stack
        self._topic = topic

    def _algo(self, bids: List, asks: List):
        """Algo implementation for calculating best bid and ask."""
        # FIXME: THIS IS INCORRECT AFTER CHANGES, need to find smallest using numpy
        best_bid = [float(bids[0][0]), float(bids[0][1])]
        best_ask = [float(asks[0][0]), float(asks[0][1])]

        logger.info(json.dumps({
            'BestBid': f'{best_bid[1]:.8f}@{best_bid[0]:.8f}',
            'BestAsk': f'{best_ask[1]:.8f}@{best_ask[0]:.8f}',
            'Delta': f'{(best_ask[0] - best_bid[0]):.8f}',
        }))

        # set spread, static pct mode for now, but really we need to shade this based on volume demand
        spread_pct = 0.01  # 1%

        # size needs to be improved obviously!!!
        return json.dumps({
            'best_bid': best_bid[0] + (best_bid[0]*spread_pct),
            'best_ask': best_ask[0] - (best_ask[0]*spread_pct),
            'best_bid_size': best_bid[1],
            'best_ask_size': best_ask[1],
        })

    async def process(self):
        """Process messages received."""
        if self._stack.length() < 1:
            return

        data = await self._stack.pop_all()
        bids = list(chain.from_iterable([d['bids'] for d in data]))
        asks = list(chain.from_iterable([d['asks'] for d in data]))

        result = self._algo(bids, asks)
        logger.info(result)

        try:
            await self._producer.send(self._topic, result.encode('utf-8'))
        except KafkaError as ex:
            logger.error(ex.args[0].str())

    async def run(self, interval: float = 1):
        """Run engine and process messages given an interval (default to 1s)."""
        while True:
            await asyncio.gather(asyncio.sleep(interval), self.process())
