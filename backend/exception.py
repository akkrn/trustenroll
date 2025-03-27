from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    server_error_exception,
)
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


async def redirect_to_login(request: Request, exc):
    return RedirectResponse(url="/admin/login", status_code=302)


async def redirect_to_dashboard(request: Request, exc):
    return RedirectResponse(url="/admin/card/list")


async def register_exception_handlers(admin_app):
    admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    # admin_app.add_exception_handler(HTTP_404_NOT_FOUND, redirect_to_dashboard)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, redirect_to_login)
