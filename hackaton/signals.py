import asyncio
import logging

from aiohttp import web, ClientSession
from motor.motor_asyncio import AsyncIOMotorClient

from hackaton.config import CONFIG
from hackaton.models import instance

log = logging.getLogger(__name__)


async def mongodb_connect(app: web.Application) -> None:
    mongodb_config = CONFIG['mongo']
    mongo_url = mongodb_config['uri']
    mongo_db = mongodb_config['db']

    mongo_client = AsyncIOMotorClient(
        mongo_url,
        io_loop=app.get('loop', asyncio.get_event_loop()),
        maxPoolSize=3,
    )
    database = mongo_client[mongo_db]
    app['mongo_client'] = mongo_client
    app['mongo_db'] = database
    instance.set_db(database)
    log.info('Connected to MongoDB')


async def disconnect_mongodb(app: web.Application) -> None:
    client = app['mongo_client']
    client.close()
    log.info('MongoDB disconnected')


async def init_client_session(app: web.Application) -> None:
    app['session'] = ClientSession()
    log.info('ClientSession initialized')


async def destroy_client_session(app: web.Application) -> None:
    session = app['session']
    await session.close()
    log.info('ClientSession closed')
