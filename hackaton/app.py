from asyncio import get_running_loop
from concurrent.futures.thread import ThreadPoolExecutor
from aiohttp.web_app import Application
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_autoreload import start
from hackaton.config import CONFIG, STATIC_PATH
from hackaton.middlewares import main_middleware
from hackaton.routes import setup_routes
from hackaton import signals


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
        app.router.add_static(CONFIG['static_root'], STATIC_PATH, name='build')
        start()
    return app
