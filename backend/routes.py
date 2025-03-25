from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

router = APIRouter()


@router.get("/admin/")
async def redirect_to_admin_dashboard():
    return RedirectResponse(url="/admin/card/list")
