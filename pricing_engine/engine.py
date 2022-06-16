import asyncio
import logging
import json
from typing import List
from itertools import chain
from aiokafka.errors import KafkaError
from pricing_engine.utils.producer import create_ck_producer
from pricing_engine.utils.stack import LockStack


logger = logging.getLogger(__name__)


class PBDEngine:
    """Pricing engine implementation based on Partial Book Depth (PBD)."""

    def __init__(self, stack: LockStack, topic: str) -> None:
        loop = asyncio.get_event_loop()
        self._producer = create_ck_producer(loop)
        self._stack = stack
        self._topic = topic

    def _algo(self, bids: List, asks: List):
        """Algo implementation for calculating best bid and ask."""

        best_bid = [float(bids[0][0]), float(bids[0][1])]
        best_ask = [float(asks[0][0]), float(asks[0][1])]

        logger.info(
            json.dumps(
                {
                    "BestBid": f"{best_bid[1]:.8f}@{best_bid[0]:.8f}",
                    "BestAsk": f"{best_ask[1]:.8f}@{best_ask[0]:.8f}",
                    "Delta": f"{(best_ask[0] - best_bid[0]):.8f}",
                }
            )
        )

        # set spread, static pct mode for now, but really we need to shade this based on volume demand
        spread_pct = 0.01  # 1%

        # size needs to be improved obviously!!!
        return json.dumps(
            {
                "best_bid": best_bid[0] + (best_bid[0] * spread_pct),
                "best_ask": best_ask[0] - (best_ask[0] * spread_pct),
                "best_bid_size": best_bid[1],
                "best_ask_size": best_ask[1],
            }
        )

    async def process(self):
        """Process messages received."""
        if self._stack.length() < 1:
            return

        data = await self._stack.pop_all()

        logger.info(data)

        bids = list(chain.from_iterable([d["bids"] for d in data]))
        asks = list(chain.from_iterable([d["asks"] for d in data]))

        sorted_bids = sorted(bids, key=lambda x: x[0], reverse=True)
        sorted_asks = sorted(asks, key=lambda x: x[0])

        #TODO: publish reconstructed orderbook to kafka

        result = self._algo(sorted_bids, sorted_asks) #best rate algo

        logger.info(result)

        try:
            await self._producer.send(self._topic, result.encode("utf-8"))
        except KafkaError as ex:
            logger.error(ex.args[0].str())

    async def run(self, interval: float = 1):
        """Run engine and process messages given an interval (default to 1s)."""
        try:
            await self._producer.start()
            while True:
                await asyncio.gather(asyncio.sleep(interval), self.process())
        finally:
            await self._producer.stop()
