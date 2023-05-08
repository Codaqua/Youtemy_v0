import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Course_Keyword, Course

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
    prefix='/course_keywords',
    tags=['course_keywords']
)

class CourseKeyword(BaseModel):
    keyword_id: int
    course_id: int
    keyword_name: str
    keyword_description: Optional[str] = None

@router.get('/', status_code=status.HTTP_200_OK)
async def get_course_keywords(db: Session = Depends(get_db)):
    course_keywords = db.query(Course_Keyword).all()
    keyword_list = []
    for keyword in course_keywords:
        keyword_dict = {
            "keyword_id": keyword.keyword_id,
            "course_id": keyword.course_id,
            "keyword_name": keyword.keyword_name,
            "keyword_description": keyword.keyword_description
        }
        keyword_list.append(keyword_dict)
    return keyword_list

class CreateCourseKeyword(BaseModel):
    course_id: int
    keyword_name: str
    keyword_description: Optional[str] = None

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course_keyword(keyword: CreateCourseKeyword, db: Session = Depends(get_db)):
    new_keyword = Course_Keyword(
        course_id=keyword.course_id,
        keyword_name=keyword.keyword_name,
        keyword_description=keyword.keyword_description
    )

    db.add(new_keyword)
    db.commit()

    return {"message": "Course keyword created successfully", "keyword_id": new_keyword.keyword_id}
