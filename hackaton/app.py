from asyncio import get_running_loop
from base64 import urlsafe_b64decode
from concurrent.futures.thread import ThreadPoolExecutor

from aiohttp_autoreload import start
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup as setup_session
from aiohttp.web_app import Application
from aiohttp.web_middlewares import normalize_path_middleware

from hackaton import signals
from hackaton.config import CONFIG, STATIC_PATH
from hackaton.middlewares import main_middleware
from hackaton.routes import setup_routes
from hackaton.lib.auth import MongoAuthorizationPolicy


async def make_app() -> Application:
    app = Application(
        middlewares=[normalize_path_middleware(), main_middleware],
        debug=CONFIG['is_debug']
    )

    app.on_startup.extend(
        [
            signals.init_client_session,
            signals.mongodb_connect,
        ]
    )

    # To run before shutdown
    app.on_cleanup.extend(
        [
            signals.destroy_client_session,
            signals.disconnect_mongodb,
        ]
    )

    setup_routes(app)
    get_running_loop().set_default_executor(ThreadPoolExecutor(max_workers=4))
    if CONFIG['is_debug']:
        # app.router.add_static(CONFIG['static_root'], STATIC_PATH, name='build')
        start()

    secret_key = urlsafe_b64decode(CONFIG['secret_key'].encode('utf-8'))
    storage = EncryptedCookieStorage(secret_key, cookie_name='session')

    setup_session(app, storage)
    setup_security(
        app,
        SessionIdentityPolicy(),
        MongoAuthorizationPolicy(),
    )

    return app
