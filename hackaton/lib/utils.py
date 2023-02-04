import typing as t

import trafaret as tr

from os import getenv
from pathlib import Path
from ruamel.yaml import safe_load


ConfigTrafaret = tr.Dict(
    host=tr.String(max_length=64),
    port=tr.Int(gt=0),
    is_debug=tr.Bool,
    static_root=tr.String(max_length=256),
    secret_key=tr.String(),
    mongo=tr.Dict(
        uri=tr.String(),
        db=tr.String(),
    )
)


def get_env(name: str) -> str:
    env = getenv(name)
    if env:
        return env
    raise RuntimeError(f'{name} not set')


def get_config(path: str | Path) -> dict[str, t.Any]:
    with open(str(path)) as stream:
        config = safe_load(stream.read())
        ConfigTrafaret.check(config)
        return config
