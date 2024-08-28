import os
from time import sleep

from src.connection import RabbitConnection

from dotenv import load_dotenv
from loguru import logger
from kombu import Exchange, Queue, Consumer

from src import config
from src import utils

load_dotenv()


def _handle_msg(body, message) -> None:
    logger.info(f'Received message: {body}')
    message.ack()


def consume() -> None:
    with RabbitConnection() as connection:
        exchange = Exchange(config.EXCHANGE_NAME, type='direct')
        queue = Queue(config.QUEUE_NAME, exchange, routing_key=config.ROUTING_KEY)

        with connection.channel() as channel:
            exchange.maybe_bind(channel)
            queue.maybe_bind(channel)
            exchange.declare()
            queue.declare()
            channel.basic_qos(prefetch_size=0, prefetch_count=utils.to_num(config.PREFETCH_COUNT), a_global=False)

            consumer = Consumer(channel, [queue], prefetch_count=utils.to_num(config.PREFETCH_COUNT), accept=['json'])
            consumer.register_callback(_handle_msg)
            try:
                while True:
                    with consumer:
                        connection.drain_events(timeout=2)
                        sleep(utils.to_num(config.DRAIN_TIMEOUT))
            except TimeoutError:
                logger.info('Message has ended')


if __name__ == '__main__':
    consume()
