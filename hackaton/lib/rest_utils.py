import typing as t
from http import client as httplib

from aiohttp import web


def ok_response(
    code: int = httplib.OK,
    payload: dict[str, t.Any] | None = None,
) -> web.Response:
    data = dict(
        status='success',
        payload=payload or {},
        errors=None,
    )

    return web.json_response(data, status=code)


def error_response(
    code: int,
    payload: dict[str, t.Any] | None = None,
    errors_mapping: dict[str, t.Any] | None = None,
) -> web.Response:
    errors = errors_mapping or {}

    def _prepare_errors(errors: dict[str, t.Any]):
        resp_error = []
        for k, v in errors.items():
            if isinstance(v, str):
                resp_error.append({'name': k, 'value': v})
            elif isinstance(v, list):
                resp_error.append({'name': k, 'value': v[0]})

        return resp_error

    data = dict(
        status='error',
        payload=payload or {},
        errors=_prepare_errors(errors),
    )

    return web.json_response(data, status=code)
