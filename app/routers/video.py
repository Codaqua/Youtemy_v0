import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Video, Course_Sections

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/videos',
    tags=['videos']
)

class VideoModel(BaseModel):
    video_id: int
    section_id: int
    video_name: str
    video_order: int
    video_text_content: Optional[str] = None
    video_url: Optional[str] = None
    duration_sec: int
    created_at: datetime
    updated_at: Optional[datetime] = None

@router.get('/', status_code=status.HTTP_200_OK)
async def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    video_list = []
    for video in videos:
        video_dict = {
            "video_id": video.video_id,
            "section_id": video.section_id,
            "video_name": video.video_name,
            "video_order": video.video_order,
            "video_text_content": video.video_text_content,
            "video_url": video.video_url,
            "duration_sec": video.duration_sec,
            "created_at": video.created_at,
            "updated_at": video.updated_at
        }
        video_list.append(video_dict)
    return video_list

class CreateVideo(BaseModel):
    section_id: int
    video_name: str
    video_order: int
    video_text_content: Optional[str] = None
    video_url: Optional[str] = None
    duration_sec: int

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_video(video: CreateVideo, db: Session = Depends(get_db)):
    new_video = Video(
        section_id=video.section_id,
        video_name=video.video_name,
        video_order=video.video_order,
        video_text_content=video.video_text_content,
        video_url=video.video_url,
        duration_sec=video.duration_sec
    )

    db.add(new_video)
    db.commit()

    return {"message": "Video created successfully", "video_id": new_video.video_id}
