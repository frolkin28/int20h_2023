import typing as t

from marshmallow import Schema, ValidationError, fields


class ListOrOne(fields.List):
    def _deserialize(
        self, value: t.Any, attr: t.Any, data: t.Any, **kwargs: t.Any
    ) -> t.List[t.Any]:
        if value and not isinstance(value, list):
            value = [value]
        return super(ListOrOne, self)._deserialize(value, attr, data, **kwargs)
