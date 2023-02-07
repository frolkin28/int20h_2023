import typing as t
from dataclasses import dataclass

import trafaret as tr

from hackaton.lib.exceptions import SchemaValidationError


IndredientSchema = tr.Dict(
    title=tr.String(max_length=256),
    description=tr.String(max_length=2000),
    type=tr.String(max_length=120)
)

IndredientTypeSchema = tr.Dict(
    title=tr.String(max_length=256),
    description=tr.String(max_length=512),
)


@dataclass(slots=True, frozen=True)
class IngredientPayload:
    title: str
    description: str
    type: str

    @classmethod
    def load(cls, data: dict) -> 'IngredientPayload':
        try:
            IndredientSchema.check(data)
        except tr.DataError as e:
            raise SchemaValidationError(e.as_dict())

        return cls(**data)

    def to_dict(self) -> dict[str, str]:
        return dict(
            title=self.title,
            description=self.description,
            type=self.type,
        )


@dataclass(slots=True, frozen=True)
class IngredientTypePayload:
    title: str
    description: str

    @classmethod
    def load(cls, data: dict) -> 'IngredientTypePayload':
        try:
            IndredientTypeSchema.check(data)
        except tr.DataError as e:
            raise SchemaValidationError(e.as_dict())

        return cls(**data)

    def to_dict(self) -> dict[str, str]:
        return dict(
            title=self.title,
            description=self.description,
        )
