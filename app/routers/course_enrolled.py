import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Course_Enrolled

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
    prefix='/course_enrolled',
    tags=['course_enrolled']
)

class CourseEnrollment(BaseModel):
    enrolled_courses_id: int
    user_id: int
    course_id: int
    progression_status: float
    created_at: datetime

@router.get('/', status_code=status.HTTP_200_OK)
async def get_course_enrollments(db: Session = Depends(get_db)):
    course_enrollments = db.query(Course_Enrolled).all()
    enrollment_list = []
    for enrollment in course_enrollments:
        enrollment_dict = {
            "enrolled_courses_id": enrollment.enrolled_courses_id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "progression_status": enrollment.progression_status,
            "created_at": enrollment.created_at
        }
        enrollment_list.append(enrollment_dict)
    return enrollment_list

class CreateCourseEnrollment(BaseModel):
    user_id: int
    course_id: int
    progression_status: float

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course_enrollment(enrollment: CreateCourseEnrollment, db: Session = Depends(get_db)):
    new_enrollment = Course_Enrolled(
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
        progression_status=enrollment.progression_status,
        created_at=datetime.utcnow()
    )

    db.add(new_enrollment)
    db.commit()

    return {"message": "Course enrollment created successfully", "enrollment_id": new_enrollment.enrolled_courses_id}
