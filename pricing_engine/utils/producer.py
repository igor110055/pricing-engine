import asyncio
from os import getenv
from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

ssl_context = create_ssl_context()


def create_ck_producer(loop: asyncio.AbstractEventLoop):
    """Create and return Kafka consumer."""
    return AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=getenv('CK_SERVER'),
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        sasl_plain_username=getenv('CK_USER'),
        sasl_plain_password=getenv('CK_PWD'),
        ssl_context=ssl_context,
    )
