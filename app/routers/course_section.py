import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Course_Sections

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
    prefix='/course_sections',
    tags=['course_sections']
)

class CourseSection(BaseModel):
    section_id: int
    course_id: int
    section_order: int
    section_name: str
    section_description: Optional[str] = None

@router.get('/', status_code=status.HTTP_200_OK)
async def get_course_sections(db: Session = Depends(get_db)):
    sections = db.query(Course_Sections).all()
    section_list = []
    for section in sections:
        section_dict = {
            "section_id": section.section_id,
            "course_id": section.course_id,
            "section_order": section.section_order,
            "section_name": section.section_name,
            "section_description": section.section_description
        }
        section_list.append(section_dict)
    return section_list

class CreateCourseSection(BaseModel):
    course_id: int
    section_order: int
    section_name: str
    section_description: Optional[str] = None

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course_section(section: CreateCourseSection, db: Session = Depends(get_db)):
    new_section = Course_Sections(
        course_id=section.course_id,
        section_order=section.section_order,
        section_name=section.section_name,
        section_description=section.section_description
    )

    db.add(new_section)
    db.commit()

    return {"message": "Course section created successfully", "section_id": new_section.section_id}
