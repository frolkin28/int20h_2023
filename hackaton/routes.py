from aiohttp import web

from hackaton.handlers.health import health_check
from hackaton.handlers.admin import migration
from hackaton.handlers.auth import register
from hackaton.handlers.auth import login
from hackaton.handlers.auth import logout
from hackaton.handlers.user import get_user_data
from hackaton.handlers.index import index
from hackaton.handlers.recipe import recipe_view


def setup_routes(app: web.Application) -> None:
    # health check
    app.router.add_get('/health', health_check)

    # admin routes
    app.router.add_get(
        '/admin/migration/recipe_categories',
        migration.migrate_recipe_categories
    )
    app.router.add_get(
        '/admin/migration/ingredients',
        migration.migrate_ingredients
    )
    app.router.add_get(
        '/admin/migration/migrate_recipes_by_categories',
        migration.migrate_recipes_by_categories
    )
    app.router.add_get(
        '/admin/migration/mealdb_full_migration',
        migration.mealdb_full_migration
    )

    # auth routes
    app.router.add_post('/auth/register', register)
    app.router.add_post('/auth/login', login)
    app.router.add_post('/auth/logout', logout)

    app.router.add_get('/api/user', get_user_data)
    app.router.add_get(r'/api/recipe/{id:\w+}', recipe_view)

    # template routes
    app.router.add_get('/', index)
    app.router.add_get('/{tail:(?!(api|auth|admin)/)(.+)}/', index)
