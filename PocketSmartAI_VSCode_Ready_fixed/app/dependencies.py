from fastapi import Cookie, HTTPException, Request

from app.auth import decode_access_token
from app.database import get_db


def get_user_by_id(user_id: int):
    with get_db() as db:
        row = db.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def resolve_token(
    request: Request,
    access_token: str | None = Cookie(default=None),
) -> str | None:
    if access_token:
        return access_token

    authorization = request.headers.get("Authorization", "")
    if authorization.lower().startswith("bearer "):
        return authorization[7:].strip()

    return None


def get_optional_user(
    request: Request,
    access_token: str | None = Cookie(default=None),
):
    token = resolve_token(request, access_token)
    if not token:
        return None

    user_id = decode_access_token(token)
    if not user_id:
        return None

    return get_user_by_id(user_id)


def current_user(
    request: Request,
    access_token: str | None = Cookie(default=None),
):
    user = get_optional_user(request, access_token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )
    return user
