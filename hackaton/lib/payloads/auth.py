from dataclasses import dataclass

import trafaret as tr

from hackaton.lib.exceptions import SchemaValidationError


RegisterSchema = tr.Dict(
    email=tr.Email,
    password=tr.String(max_length=60),
    first_name=tr.String(max_length=120),
    last_name=tr.String(max_length=120),
)

LoginSchema = tr.Dict(
    email=tr.Email,
    password=tr.String(max_length=60),
)


@dataclass
class UserPayload:
    email: str
    password: str
    first_name: str
    last_name: str

    @classmethod
    def load(cls, data: dict) -> 'UserPayload':
        try:
            RegisterSchema.check(data)
        except tr.DataError as e:
            raise SchemaValidationError(e.as_dict())

        return cls(**data)

    def to_dict(self) -> dict[str, str]:
        return dict(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )


@dataclass
class LoginPayload:
    email: str
    password: str

    @classmethod
    def load(cls, data: dict) -> 'LoginPayload':
        try:
            LoginSchema.check(data)
        except tr.DataError as e:
            raise SchemaValidationError(e.as_dict())

        return cls(**data)
