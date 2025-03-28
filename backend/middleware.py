import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import uuid

from models import VisitLog

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
        logger.info(f"{request.method} {path} - IP: {client_ip} - Status: {response.status_code}")
    else:
        response = await call_next(request)

    return response


class RealIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            # Безопасное извлечение IP с обработкой исключений
            real_ip = await self.extract_real_ip(request)

            # Устанавливаем IP в объект request.state
            request.state.real_ip = real_ip

            # Логируем для отладки
            logger.info(f"Extracted IP: {real_ip}")

            response = await call_next(request)
            return response

        except Exception as e:
            # Обработка любых непредвиденных ошибок
            logger.error(f"Error in RealIPMiddleware: {str(e)}", exc_info=True)

            # Возвращаем оригинальный клиентский хост в случае ошибки
            try:
                request.state.real_ip = request.client.host
            except Exception:
                request.state.real_ip = "unknown"

            # Пропускаем middleware без остановки приложения
            return await call_next(request)

    async def extract_real_ip(self, request: Request) -> str:
        try:
            # Безопасное извлечение заголовков
            forwarded_for = request.headers.get("X-Forwarded-For")
            real_ip_header = request.headers.get("X-Real-IP")

            # Список для хранения потенциальных IP
            potential_ips = []

            # Обработка X-Forwarded-For
            if forwarded_for:
                potential_ips.extend([ip.strip() for ip in forwarded_for.split(",") if ip and ip.strip()])

            # Добавляем X-Real-IP, если есть
            if real_ip_header:
                potential_ips.append(real_ip_header)

            # Добавляем клиентский хост как последний вариант
            potential_ips.append(request.client.host)

            # Фильтрация и валидация IP
            valid_ips = self.filter_valid_ips(potential_ips)

            # Возвращаем первый валидный IP или генерируем уникальный идентификатор
            return valid_ips[0] if valid_ips else str(uuid.uuid4())

        except Exception as e:
            logger.warning(f"IP extraction failed: {str(e)}")
            return str(uuid.uuid4())

    def filter_valid_ips(self, ips: list) -> list:
        """
        Фильтрует список IP-адресов, исключая приватные и локальные
        """

        def is_valid_ip(ip: str) -> bool:
            # Список масок приватных и локальных сетей
            private_prefixes = [
                "127.",
                "10.",
                "172.16.",
                "172.17.",
                "172.18.",
                "172.19.",
                "172.20.",
                "172.21.",
                "172.22.",
                "172.23.",
                "172.24.",
                "172.25.",
                "172.26.",
                "172.27.",
                "172.28.",
                "172.29.",
                "172.30.",
                "172.31.",
                "192.168.",
                "::1",
                "localhost",
            ]

            # Проверяем, не начинается ли IP с приватных префиксов
            return not any(ip.startswith(prefix) for prefix in private_prefixes)

        # Возвращаем список валидных IP
        return [ip for ip in ips if is_valid_ip(ip)]
