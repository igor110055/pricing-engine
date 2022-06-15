import logging
import asyncio
from os import getenv
from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context
from fastapi import FastAPI, WebSocket
from websockets.exceptions import WebSocketException

logger = logging.getLogger(__name__)
ssl_context = create_ssl_context()

app = FastAPI()


def create_ck_consumer(topic: str, loop: asyncio.AbstractEventLoop):
    """Create and return Kafka consumer."""
    return AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers=getenv("CK_SERVER"),
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username=getenv("CK_USER"),
        sasl_plain_password=getenv("CK_PWD"),
        ssl_context=ssl_context,
    )


@app.websocket("/ws/{topic}")
async def ws_price_publisher(websocket: WebSocket, topic: str):
    """Price publisher websocket endpoint."""
    await websocket.accept()
    logger.info("Client Connected!")

    loop = asyncio.get_event_loop()
    consumer = create_ck_consumer(topic, loop)

    await consumer.start()

    try:
        async for msg in consumer:
            data = msg.value.decode("utf-8")
            await websocket.send_text(data)

    except WebSocketException:
        logger.info("Disconnected by client.")
    finally:
        await consumer.stop()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
