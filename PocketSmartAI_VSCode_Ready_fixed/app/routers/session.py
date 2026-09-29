from fastapi import APIRouter, Depends, Request

from app.database import get_db
from app.dependencies import current_user, get_optional_user


router = APIRouter(tags=["session"])


@router.get("/api/session-info")
def session_info(request: Request):
    user = get_optional_user(
        request,
        request.cookies.get("access_token"),
    )

    return {
        "logged_in": bool(user),
        "user": user,
    }


@router.get("/api/session-data")
def session_data(user=Depends(current_user)):
    with get_db() as db:
        total = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM recommendations
            WHERE user_id = ?
            """,
            (user["id"],),
        ).fetchone()["count"]

        rows = db.execute(
            """
            SELECT planner, COUNT(*) AS count
            FROM recommendations
            WHERE user_id = ?
            GROUP BY planner
            """,
            (user["id"],),
        ).fetchall()

    return {
        "user": user,
        "total_recommendations": int(total),
        "planner_counts": {
            row["planner"]: int(row["count"])
            for row in rows
        },
    }
