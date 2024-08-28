import os

from dotenv import load_dotenv

load_dotenv()

ROUTING_KEY = os.getenv('ROUTING_KEY', 'test_routing_key')
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME', 'test_exchange')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
DRAIN_TIMEOUT = os.getenv('DRAIN_TIMEOUT', 2)
PREFETCH_COUNT = os.getenv('PREFETCH_COUNT', 5)
