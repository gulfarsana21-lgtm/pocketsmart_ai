import json
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from PIL import Image, UnidentifiedImageError

from app.config import settings
from app.database import get_db
from app.dependencies import current_user
from app.schemas import HomeRequest, PartyRequest
from app.services.recommendation_service import get_recommendations


router = APIRouter(prefix="/api/planners", tags=["planners"])


class PlannerError(Exception):
    pass


def save_history(user_id: int, planner: str, payload: dict, result: dict) -> int:
    with get_db() as db:
        cursor = db.execute(
            """
            INSERT INTO recommendations
                (user_id, planner, input_json, result_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                planner,
                json.dumps(payload, ensure_ascii=False),
                json.dumps(result, ensure_ascii=False),
            ),
        )
        return int(cursor.lastrowid)


@router.post("/home")
def home_planner(
    payload: HomeRequest,
    user=Depends(current_user),
):
    rooms = [room.strip() for room in payload.rooms if room.strip()]

    if not rooms:
        raise HTTPException(
            status_code=422,
            detail="Please provide at least one room.",
        )

    data = payload.model_dump()
    data["rooms"] = rooms

    result = get_recommendations("home", data)
    history_id = save_history(user["id"], "home", data, result)
    result["history_id"] = history_id
    return result


@router.post("/party")
def party_planner(
    payload: PartyRequest,
    user=Depends(current_user),
):
    data = payload.model_dump()
    result = get_recommendations("party", data)
    history_id = save_history(user["id"], "party", data, result)
    result["history_id"] = history_id
    return result


@router.post("/jewelry")
async def jewelry_planner(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Elegant"),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(default=None),
    user=Depends(current_user),
):
    if budget <= 0 or budget > 10_000_000:
        raise HTTPException(
            status_code=422,
            detail="Budget must be between ₹1 and ₹1,00,00,000.",
        )

    occasion = occasion.strip()
    style = style.strip() or "Elegant"
    outfit_description = outfit_description.strip()

    if len(occasion) < 2:
        raise HTTPException(
            status_code=422,
            detail="Occasion is required.",
        )

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_description": outfit_description,
    }

    image_path: Path | None = None

    if outfit_image and outfit_image.filename:
        allowed_types = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }

        extension = allowed_types.get(outfit_image.content_type or "")

        if not extension:
            raise HTTPException(
                status_code=415,
                detail="Only JPG, PNG and WEBP images are supported.",
            )

        content = await outfit_image.read()
        max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024

        if len(content) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image must be smaller than "
                    f"{settings.MAX_UPLOAD_MB} MB."
                ),
            )

        image_path = settings.UPLOAD_DIR / f"{uuid.uuid4().hex}{extension}"
        image_path.write_bytes(content)

        try:
            with Image.open(image_path) as image:
                image.verify()
        except (UnidentifiedImageError, OSError):
            image_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid image.",
            )

    try:
        result = get_recommendations(
            "jewelry",
            data,
            image_path=str(image_path) if image_path else None,
        )
        history_id = save_history(
            user["id"],
            "jewelry",
            data,
            result,
        )
        result["history_id"] = history_id
        return result
    finally:
        if image_path:
            image_path.unlink(missing_ok=True)
