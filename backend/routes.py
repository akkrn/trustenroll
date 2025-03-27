from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
@router.get("/admin/")
async def redirect_to_admin_dashboard():
    return RedirectResponse(url="/admin/card/list")
