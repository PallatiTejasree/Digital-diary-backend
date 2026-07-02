from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.reflection import router as reflection_router
from app.database import Base, engine
import app.models

from app.models import User
from app.auth import get_current_user

from app.users import router as user_router
from app.diary import router as diary_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Diary Backend")

# ----------------------------
# CORS Configuration
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://digital-diary-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Register routers
# ----------------------------
app.include_router(user_router)
app.include_router(diary_router)
app.include_router(reflection_router)

# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "Digital Diary Backend Running 🚀"
    }

# ----------------------------
# Current logged-in user
# ----------------------------
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }