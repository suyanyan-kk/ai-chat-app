from fastapi import APIRouter
from app.schemas.request import TitleRequest
from app.llm.services.title_service import generate_title

router = APIRouter()

@router.post("/generate_title")
async def generate_title_api(req: TitleRequest):
    title = generate_title(req.message)
    return {"title": title.strip()}