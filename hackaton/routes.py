import aiohttp_cors
from aiohttp import web

from hackaton.handlers.health import health_check
from hackaton.handlers.auth import register
from hackaton.handlers.auth import login
from hackaton.handlers.auth import logout
from hackaton.handlers.user import get_user_data
from hackaton.handlers.index import index
from hackaton.handlers.recipe import create_recipe_category_handler, recipe_view
from hackaton.handlers.search import search_recipe
from hackaton.handlers.search import search_ingredient
from hackaton.handlers.ingredient import add_ingredient
from hackaton.handlers.ingredient import add_user_product
from hackaton.handlers.ingredient import delete_user_product
from hackaton.handlers.ingredient import get_ingredient_type_list
from hackaton.handlers.ingredient import create_ingredient_type_handler
from hackaton.config import CONFIG


def setup_routes(app: web.Application) -> None:
    # health check
    app.router.add_get('/health', health_check)

    # auth routes
    app.router.add_post('/auth/register', register)
    app.router.add_post('/auth/login', login)
    app.router.add_post('/auth/logout', logout)

    app.router.add_get('/api/user', get_user_data)
    app.router.add_get(r'/api/recipe/{id:\w+}', recipe_view)
    app.router.add_post('/api/ingredient', add_ingredient)
    app.router.add_post('/api/user/product', add_user_product)
    app.router.add_delete('/api/user/product', delete_user_product)

    app.router.add_post('/api/recipe/search', search_recipe)
    app.router.add_post('/api/ingredient/search', search_ingredient)
    app.router.add_get('/api/ingredient_types', get_ingredient_type_list)
    app.router.add_post('/api/ingredient_type', create_ingredient_type_handler)
    app.router.add_post('/api/recipe_category', create_recipe_category_handler)

    # template routes
    app.router.add_get('/', index)
    app.router.add_get('/{tail:(?!(api|auth|admin)/)(.+)}/', index)

    if CONFIG['is_debug']:
        # Configure default CORS settings.
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods='*',
            )
        })

        # Configure CORS on all routes.
        for route in list(app.router.routes()):
            cors.add(route)
