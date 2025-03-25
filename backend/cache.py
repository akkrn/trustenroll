import logging
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi_cache import FastAPICache

logger = logging.getLogger(__name__)
GLOBAL_CACHE_EXPIRE = 60


class CacheRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            cache_key = f"cache:{request.method}:{str(request.url)}"
            cache = FastAPICache.get_backend()
            cached = await cache.get(cache_key)
            if cached:
                return Response(content=cached, media_type="application/json")
            response: Response = await original_handler(request)
            if response.status_code == 200:
                await cache.set(cache_key, response.body, expire=GLOBAL_CACHE_EXPIRE)
            return response

        return custom_route_handler
