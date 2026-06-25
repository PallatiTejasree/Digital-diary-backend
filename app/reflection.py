from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import DiaryEntry
from .auth import get_current_user

router = APIRouter(
    prefix="/reflection",
    tags=["Reflection"]
)


@router.get("/")
def generate_reflection(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    diaries = (
        db.query(DiaryEntry)
        .filter(DiaryEntry.user_id == current_user.id)
        .order_by(DiaryEntry.created_at.desc())
        .all()
    )

    if not diaries:
        return {
            "reflection": "You haven't written any diary entries yet."
        }

    latest = diaries[0]

    return {
        "latest_title": latest.title,
        "latest_mood": latest.mood,
        "reflection": f"You recently felt '{latest.mood}' while writing '{latest.title}'. Keep reflecting and tracking your emotions."
    }