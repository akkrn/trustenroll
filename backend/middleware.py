import logging

from fastapi import Request

logger = logging.getLogger("custom.access")

EXCLUDED_PATHS = (
    "/static/",
    "/favicon.ico",
    "/images/",
    "/img/",
    "/manifest.json/",
)


async def log_ip_middleware(request: Request, call_next):
    path = request.url.path

    if not path.startswith(EXCLUDED_PATHS):
        client_ip = request.client.host
        response = await call_next(request)
        logger.info(
            f"{request.method} {path} - IP: {client_ip} - Status: {response.status_code}"
        )
    else:
        response = await call_next(request)

    return response
