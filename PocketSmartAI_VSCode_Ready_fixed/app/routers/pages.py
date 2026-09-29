import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.dependencies import get_optional_user


router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = get_optional_user(
        request,
        request.cookies.get("access_token"),
    )

    if not user:
        return RedirectResponse(
            url="/login?next=/dashboard",
            status_code=303,
        )

    with get_db() as db:
        rows = db.execute(
            """
            SELECT id, planner, result_json, created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 6
            """,
            (user["id"],),
        ).fetchall()

    recent = []
    for row in rows:
        result = json.loads(row["result_json"])
        recent.append(
            {
                "id": row["id"],
                "planner": row["planner"],
                "title": result.get("title", "Recommendation plan"),
                "created_at": row["created_at"],
            }
        )

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user,
            "recent": recent,
        },
    )


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    user = get_optional_user(
        request,
        request.cookies.get("access_token"),
    )

    if not user:
        return RedirectResponse(
            url="/login?next=/history",
            status_code=303,
        )

    with get_db() as db:
        rows = db.execute(
            """
            SELECT id, planner, result_json, created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user["id"],),
        ).fetchall()

    history = []
    for row in rows:
        result = json.loads(row["result_json"])
        history.append(
            {
                "id": row["id"],
                "planner": row["planner"],
                "title": result.get("title", "Recommendation plan"),
                "created_at": row["created_at"],
            }
        )

    return templates.TemplateResponse(
        request,
        "history.html",
        {
            "user": user,
            "history": history,
        },
    )


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner_page(request: Request, planner: str):
    if planner not in {"home", "party", "jewelry"}:
        return HTMLResponse("Planner not found", status_code=404)

    return templates.TemplateResponse(
        request,
        "planner.html",
        {"planner": planner},
    )


@router.get("/recommendations/{history_id}", response_class=HTMLResponse)
def recommendation_page(request: Request, history_id: int):
    user = get_optional_user(
        request,
        request.cookies.get("access_token"),
    )

    if not user:
        return RedirectResponse(
            url=f"/login?next=/recommendations/{history_id}",
            status_code=303,
        )

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
        return HTMLResponse(
            "Recommendation not found",
            status_code=404,
        )

    return templates.TemplateResponse(
        request,
        "recommendations.html",
        {
            "user": user,
            "history_id": history_id,
            "planner": row["planner"],
            "input": json.loads(row["input_json"]),
            "result": json.loads(row["result_json"]),
        },
    )
