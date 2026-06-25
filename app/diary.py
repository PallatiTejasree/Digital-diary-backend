from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import DiaryEntry
from .schemas import DiaryCreate, DiaryUpdate, DiaryResponse
from .auth import get_current_user

router = APIRouter(prefix="/diary", tags=["Diary"])
@router.post("/", response_model=DiaryResponse)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_diary = DiaryEntry(
    user_id=current_user.id,
    title=diary.title,
    content=diary.content,
    mood=diary.mood,
    category=diary.category,
    is_favorite=diary.is_favorite,
    is_archived=diary.is_archived,
    )

    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)

    return new_diary
@router.get("/", response_model=list[DiaryResponse])
def get_diaries(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return (
        db.query(DiaryEntry)
        .filter(DiaryEntry.user_id == current_user.id)
        .order_by(DiaryEntry.created_at.desc())
        .all()
    )
@router.get("/{id}", response_model=DiaryResponse)
def get_diary(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    diary = (
        db.query(DiaryEntry)
        .filter(
            DiaryEntry.id == id,
            DiaryEntry.user_id == current_user.id,
        )
        .first()
    )

    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    return diary
@router.put("/{id}", response_model=DiaryResponse)
def update_diary(
    id: int,
    diary_data: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    diary = (
        db.query(DiaryEntry)
        .filter(
            DiaryEntry.id == id,
            DiaryEntry.user_id == current_user.id,
        )
        .first()
    )

    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary_data.title is not None:
        diary.title = diary_data.title

    if diary_data.content is not None:
        diary.content = diary_data.content

    if diary_data.mood is not None:
        diary.mood = diary_data.mood
    if diary_data.category is not None:
        diary.category = diary_data.category
        diary.is_favorite = diary_data.is_favorite
        diary.is_archived = diary_data.is_archived
    if diary_data.is_favorite is not None:
        diary.is_favorite = diary_data.is_favorite

    db.commit()
    db.refresh(diary)

    return diary
@router.delete("/{id}")
def delete_diary(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    diary = (
        db.query(DiaryEntry)
        .filter(
            DiaryEntry.id == id,
            DiaryEntry.user_id == current_user.id,
        )
        .first()
    )

    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    db.delete(diary)
    db.commit()

    return {"message": "Diary deleted successfully"}