import os

from loguru import logger
from kombu import Connection
from dotenv import load_dotenv


load_dotenv()


class RabbitConnection:
    RABBIT_URL = os.getenv('RABBIT_URL')

    def __init__(self, url=None):
        if url:
            self.RABBIT_URL = url
        self.connection = None

    def __enter__(self):
        self.connection = Connection(self.RABBIT_URL)
        self.connection.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            logger.info('Connection closed')
            self.connection.close()
        else:
            logger.error(f'Connection closed. Errors: {exc_type}')
            self.connection.close()
