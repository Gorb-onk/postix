import os

from dotenv import load_dotenv
from aiocache import caches, SimpleMemoryCache

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')

TELEGRAM_ADMIN_SESSION_PATH = os.getenv('TELEGRAM_ADMIN_SESSION_PATH')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': REDIS_HOST,
        'port': REDIS_PORT,
        'timeout': 1,
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'plugins': []
    },
    'test': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'plugins': []
    },
})

