from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, PasswordReset, PinRecovery
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/recover-account")
def recover_account(request: PinRecovery, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.pin_hash.isnot(None)).all()
    for user in users:
        if verify_password(request.pin, user.pin_hash):
            return {"name": user.name, "email": user.email}
    raise HTTPException(status_code=404, detail="PIN not found")


@router.post("/reset-password")
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="No account found for this email")
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    db_user.password_hash = hash_password(request.new_password)
    db.commit()

    return {"message": "Password reset successfully"}


@router.post("/change-password")
def change_password(
    request: PasswordReset,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    current_user.password_hash = hash_password(request.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


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
        password_hash=hashed,
        pin_hash=hash_password(user.pin),
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
