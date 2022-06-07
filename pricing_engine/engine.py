import logging
import json
from websockets import connect
from websockets.exceptions import ConnectionClosed

logger = logging.getLogger(__name__)


async def process(message):
    event = json.loads(message)
    logger.info(event)

    # TODO: perform functions here
    # TODO: send to kafka


async def main(uri):
    async for websocket in connect(uri):
        logger.info(f'Connected to {uri}')
        try:
            async for message in websocket:
                await process(message)
        except ConnectionClosed:
            logger.info(f'Disconnected from {uri}, trying to reconnect...')
            continue
