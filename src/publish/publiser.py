import os
from time import sleep

from dotenv import load_dotenv
from loguru import logger
from kombu import Exchange, Queue, Producer
from src.connection import RabbitConnection


load_dotenv()
ROUTING_KEY = os.getenv('ROUTING_KEY', 'test_routing_key')
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME', 'test_exchange')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
MESSAGE_COUNT = os.getenv('MESSAGE_COUNT', '')
SLEEP_TIME = int(os.getenv('SLEEP_TIME', 3))


def has_connect():
    with RabbitConnection() as connection:
        return connection.connected


def publish() -> None:
    with RabbitConnection() as connection:
        exchange = Exchange(EXCHANGE_NAME, type='direct')
        queue = Queue(QUEUE_NAME, exchange, routing_key=ROUTING_KEY)

        with connection.channel() as channel:
            exchange.maybe_bind(channel)
            queue.maybe_bind(channel)
            exchange.declare()
            queue.declare()

            producer = Producer(channel)
            _publish(producer)


def _publish(producer: Producer) -> None:
    if not MESSAGE_COUNT:
        cnt = 0
        while True:
            cnt += 1
            producer.publish({'message': f'message {cnt}'}, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
            logger.info(f'Message {cnt} has been published')
            sleep(SLEEP_TIME)
    else:
        for i in range(1, int(MESSAGE_COUNT)):
            producer.publish({'message': f'message {i}'}, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
            logger.info(f'Message {i} has been published')
            sleep(SLEEP_TIME)


print(has_connect())
