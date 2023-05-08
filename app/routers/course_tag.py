import sys
sys.path.append("..")

from typing import List, Optional
import app.models as models
from app.models import Course_Tag

from pydantic import BaseModel, validator
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
    prefix='/course_tags',
    tags=['course_tags']
)

class CourseTag(BaseModel):
    course_tag_id: int
    course_id: int
    tag_id: int

@router.get('/', status_code=status.HTTP_200_OK)
async def get_course_tags(db: Session = Depends(get_db)):
    course_tags = db.query(Course_Tag).all()
    course_tag_list = []
    for course_tag in course_tags:
        course_tag_dict = {
            "course_tag_id": course_tag.course_tag_id,
            "course_id": course_tag.course_id,
            "tag_id": course_tag.tag_id
        }
        course_tag_list.append(course_tag_dict)
    return course_tag_list


class CourseTagCreate(BaseModel):
    course_id: int
    center_id: Optional[int] = None
    study_id: Optional[int] = None
    subject_id: Optional[int] = None
    grade_id: Optional[int] = None
    
    # Transform 0 to None, if not it gives error
    @validator('center_id', 'study_id', 'subject_id', 'grade_id', pre=True)
    def transform_zero_to_none(cls, value):
        return None if value == 0 else value

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course_tag(course_tag: CourseTagCreate, db: Session = Depends(get_db)):
    new_course_tag = Course_Tag(
        course_id=course_tag.course_id,
        center_id=course_tag.center_id,
        study_id=course_tag.study_id,
        subject_id=course_tag.subject_id,
        grade_id=course_tag.grade_id,
    )
    db.add(new_course_tag)
    db.commit()
    return {"message": "Course tag created successfully", "course_tag_id": new_course_tag.course_tag_id}


# class CreateCourseTag(BaseModel):
#     course_id: int
#     tag_id: int

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_course_tag(course_tag: CreateCourseTag, db: Session = Depends(get_db)):
#     new_course_tag = Course_Tag(
#         course_id=course_tag.course_id,
#         tag_id=course_tag.tag_id
#     )

#     db.add(new_course_tag)
#     db.commit()

#     return {"message": "Course tag created successfully", "course_tag_id": new_course_tag.course_tag_id}
