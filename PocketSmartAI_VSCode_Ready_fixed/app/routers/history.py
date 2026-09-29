import json

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.dependencies import current_user


router = APIRouter(prefix="/api/history", tags=["history"])


def convert_row(row):
    return {
        "id": int(row["id"]),
        "planner": row["planner"],
        "input": json.loads(row["input_json"]),
        "result": json.loads(row["result_json"]),
        "created_at": row["created_at"],
    }


@router.get("")
def get_history(user=Depends(current_user)):
    with get_db() as db:
        rows = db.execute(
            """
            SELECT id, planner, input_json, result_json, created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user["id"],),
        ).fetchall()

    return [convert_row(row) for row in rows]


@router.get("/{history_id}")
def get_history_item(
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
            detail="History item not found.",
        )

    return convert_row(row)


@router.delete("/{history_id}")
def delete_history(
    history_id: int,
    user=Depends(current_user),
):
    with get_db() as db:
        cursor = db.execute(
            """
            DELETE FROM recommendations
            WHERE id = ? AND user_id = ?
            """,
            (history_id, user["id"]),
        )

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="History item not found.",
        )

    return {
        "message": "History item deleted.",
        "id": history_id,
    }
