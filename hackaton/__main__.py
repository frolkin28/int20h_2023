if __name__ == '__main__':
    import logging
    import sys

    from aiohttp.web import run_app
    from uvloop import install

    from hackaton.app import make_app
    from hackaton.config import CONFIG

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info('{} started'.format('hackaton'))
    install()
    run_app(make_app(), port=CONFIG['port'])
