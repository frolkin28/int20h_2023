if __name__ == '__main__':
    from aiohttp.web import run_app
    from uvloop import install
    from hackaton.app import make_app
    from hackaton.config import CONFIG
    from logevo import configure_logging
    from logging import info

    configure_logging()
    info('{} started'.format('hackaton'))
    install()
    run_app(make_app(), port=CONFIG['port'])
