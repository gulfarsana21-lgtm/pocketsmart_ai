import json

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.dependencies import current_user


router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/recommendations-details/{history_id}")
def recommendation_details(
    history_id: int,
    user=Depends(current_user),
):
    with get_db() as db:
        row = db.execute(
            """
            SELECT id, planner, input_json, result_json, created_at
            FROM recommendations
            WHERE id = ? AND user_id = ?
            """,
            (history_id, user["id"]),
        ).fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation details not found.",
        )

    return {
        "id": row["id"],
        "planner": row["planner"],
        "input": json.loads(row["input_json"]),
        "result": json.loads(row["result_json"]),
        "created_at": row["created_at"],
    }
