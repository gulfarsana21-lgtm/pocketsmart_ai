from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app.dependencies import current_user
from app.schemas import LoginRequest, RegisterRequest


router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register")
def register(payload: RegisterRequest, response: Response):
    name = payload.name.strip()
    email = payload.email.lower().strip()

    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="An account with this email already exists.",
            )

        cursor = db.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, hash_password(payload.password)),
        )
        user_id = int(cursor.lastrowid)

    response.set_cookie(
        key="access_token",
        value=create_access_token(user_id),
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24,
    )

    return {
        "message": "Registration successful.",
        "user": {"id": user_id, "name": name, "email": email},
    }


@router.post("/login")
def login(payload: LoginRequest, response: Response):
    email = payload.email.lower().strip()

    with get_db() as db:
        row = db.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    response.set_cookie(
        key="access_token",
        value=create_access_token(int(row["id"])),
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24,
    )

    return {
        "message": "Login successful.",
        "user": {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
        },
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )
    return {"message": "Logged out successfully."}


@router.get("/me")
def me(user=Depends(current_user)):
    return {"user": user}
