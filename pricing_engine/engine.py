import logging
import json
from websockets import connect
from websockets.exceptions import ConnectionClosed
from confluent_kafka.error import KafkaException
from pricing_engine.producer import Producer
from pricing_engine.utils.gen_url import gen_binance_pbd_ws_url

logger = logging.getLogger(__name__)


class PBDEngine:
    """Pricing engine implementation based on Partial Book Depth (PBD)."""

    def __init__(self, producer: Producer, symbol: str, levels: int = 5, ms: bool = False) -> None:
        self._producer = producer
        self._url = gen_binance_pbd_ws_url(symbol, levels, ms)

    async def process(self, message: str):
        """
        Process message received from websocket.
        LATER: modify algo in here, better to create functions to abstract this part
        """
        data = json.loads(message)

        # Load bids & asks
        bids = data["bids"]
        asks = data["asks"]
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
        result = json.dumps({
            'best_bid': best_bid[0] + (best_bid[0]*spread_pct),
            'best_ask': best_ask[0] - (best_ask[0]*spread_pct),
            'best_bid_size': best_bid[1],
            'best_ask_size': best_ask[1],
        })
        logger.info(result)

        # Send to Kafka
        try:
            self._producer.produce("TEST_TOPIC", result.encode('utf-8'))
        except KafkaException as ex:
            logger.error(ex.args[0].str())

    async def start(self):
        async for websocket in connect(self._url):
            logger.info(f'Connected to {self._url}')
            try:
                async for message in websocket:
                    await self.process(message)
            except ConnectionClosed:
                logger.warn(f'Disconnected from {self._url}, reconnecting...')
                continue
