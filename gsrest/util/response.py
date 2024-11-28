import json

from aiohttp import web


def r(data):
    if isinstance(data, list):
        data = [d.to_dict() for d in data]
    else:
        data = data.to_dict()
    return web.Response(
        status=200, text=json.dumps(data), headers={"Content-type": "application/json"}
    )
