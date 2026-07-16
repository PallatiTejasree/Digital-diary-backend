from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter()


# -------------------------
# SIGNUP
# -------------------------
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed = hash_password(user.password)

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # # DEBUG (temporary)
    # print("===================================")
    # print("Email received:", repr(user.email))
    # print("Password received:", repr(user.password))
    # print("===================================")

    # Find user by email
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = create_access_token(
        {
            "user_id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }