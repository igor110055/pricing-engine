from os import getenv
from threading import Thread
from confluent_kafka import Producer as CKProducer


def load_ck_config():
    """
    Load env variables as confluent kafka config.
    Return Confluent Config.
    """
    return {
        'bootstrap.servers': getenv('CK_SERVER'),
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': getenv('CK_USER'),
        'sasl.password': getenv('CK_PWD'),
    }


class Producer:
    """
    Threaded Confluent Kafka Producer.
    Recommend to use as singleton.
    """

    def __init__(self, configs: dict):
        self._producer = CKProducer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic: str, value: str, on_delivery=None):
        self._producer.produce(topic, value, on_delivery=on_delivery)
