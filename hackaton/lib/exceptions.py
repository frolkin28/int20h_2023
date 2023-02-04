import typing as t


class MealDBMigrationException(Exception):
    pass


class SchemaValidationError(Exception):
    def __init__(self, errors: dict[str, t.Any]) -> None:
        self.errors = errors

    def __str__(self) -> str:
        return f'SchemaValidationError({self.errors})'


class UserAlreadyExists(Exception):
    pass
