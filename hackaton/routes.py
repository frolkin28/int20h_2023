from aiohttp import web

from hackaton.handlers.health import health_check

from hackaton.handlers.admin import migration


def setup_routes(app: web.Application) -> None:
    # health check
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)

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
