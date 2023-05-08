import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Course, Course_Sections, Centers_Enum, Studies_Enum, Subjects_Enum, Grades_Enum

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from sqlalchemy.orm import joinedload
from fastapi.responses import JSONResponse

from app.database import SessionLocal, engine

from app.schemas import CourseWithDetails, VideoSchema, CourseSectionSchema, CourseKeywordSchema, CenterSchema, StudySchema, SubjectSchema, GradeSchema, CourseTagSchema

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/courses',
    tags=['courses']
)

class CourseModel(BaseModel):
    course_id: int
    tutor_id: int
    course_name: str
    course_description: Optional[str] = None
    level_difficulty: Optional[int] = None
    total_duration: Optional[int] = None
    url: str
    created_at: datetime
    updated_at: Optional[datetime] = None

@router.get('/', status_code=status.HTTP_200_OK)
async def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    course_list = []
    for course in courses:
        course_dict = {
            "course_id": course.course_id,
            "tutor_id": course.tutor_id,
            "course_name": course.course_name,
            "course_description": course.course_description,
            "level_difficulty": course.level_difficulty,
            "total_duration": course.total_duration,
            "url": course.url,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        }
        course_list.append(course_dict)
    return course_list

class CreateCourseModel(BaseModel):
    tutor_id: int
    course_name: str
    course_description: Optional[str] = None
    level_difficulty: Optional[int] = None
    total_duration: Optional[int] = None
    url: str

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course(course: CreateCourseModel, db: Session = Depends(get_db)):
    new_course = Course(
        tutor_id=course.tutor_id,
        course_name=course.course_name,
        course_description=course.course_description,
        level_difficulty=course.level_difficulty,
        total_duration=course.total_duration,
        url=course.url,
        created_at=datetime.utcnow()
    )

    db.add(new_course)
    db.commit()

    return {"message": "Course created successfully", "course_id": new_course.course_id}


class CourseWithDetails(BaseModel):
    course_id: int
    course_name: str
    course_description: str
    level_difficulty: int

# @router.get('/all', response_model=List[CourseWithDetails])
# async def get_all_courses(db: Session = Depends(get_db)):
#     courses = (
#         db.query(models.Course)
#         .options(
#             joinedload(models.Course.course_sections)
#             .joinedload(models.Course_Sections.videos),
#             joinedload(models.Course.course_keywords),
#             joinedload(models.Course.course_tags)
#             .joinedload(models.Course_Tag.center)
#             .joinedload(models.Course_Tag.study)
#             .joinedload(models.Course_Tag.subject)
#             .joinedload(models.Course_Tag.grade),
#         )
#         .all()
#     )

#     course_list = [CourseWithDetails.from_orm(course) for course in courses]
#     return course_list

@router.get('/all', response_model=List[CourseWithDetails])
async def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course)\
        .options(
            joinedload(models.Course.course_sections).joinedload(models.Course_Sections.videos),
            joinedload(models.Course.course_keywords),
            joinedload(models.Course.course_tags)
                .joinedload(models.Course_Tag.center),
            joinedload(models.Course.course_tags)
                .joinedload(models.Course_Tag.study),
            joinedload(models.Course.course_tags)
                .joinedload(models.Course_Tag.subject),
            joinedload(models.Course.course_tags)
                .joinedload(models.Course_Tag.grade)
        )\
        .all()
    
        # Print out the courses and their related objects
    for course in courses:
        print(course)
        print(course.course_sections)
        print(course.course_keywords)
        print(course.course_tags)
    
    # return courses
    
    course_list = []

    for course in courses:
        course_sections = [CourseSectionSchema.from_orm(cs) for cs in course.course_sections]
        course_keywords = [CourseKeywordSchema.from_orm(ck) for ck in course.course_keywords]
        course_tags = [CourseTagSchema.from_orm(ct) for ct in course.course_tags]

        course_details = CourseWithDetails(
            course_id=course.course_id,
            course_name=course.course_name,
            course_description=course.course_description,
            level_difficulty=course.level_difficulty,
            course_sections=course_sections,
            course_keywords=course_keywords,
            course_tags=course_tags
        )

        course_list.append(course_details)

    return course_list
    
    # course_list = []

    # for course in courses:
    #     course_sections = [CourseSectionSchema.from_orm(cs) for cs in course.course_sections]
    #     course_keywords = [CourseKeywordSchema.from_orm(ck) for ck in course.course_keywords]
    #     course_tags = [CourseTagSchema.from_orm(ct) for ct in course.course_tags]

    #     course_details = CourseWithDetails(
    #         course_id=course.course_id,
    #         course_name=course.course_name,
    #         course_description=course.course_description,
    #         level_difficulty=course.level_difficulty,
    #         course_sections=course_sections,
    #         course_keywords=course_keywords,
    #         course_tags=course_tags
    #     )

    #     course_list.append(course_details)

    # return course_list
    
    
# @router.get('/course-sections', status_code=status.HTTP_200_OK)
# async def get_courses(db: Session = Depends(get_db)):
#     courses = db.query(Course).options(joinedload(Course.sectionsRelation)).all()
#     return courses

@router.get('/course-sections', status_code=status.HTTP_200_OK)
async def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).options(joinedload(models.Course.sectionsRelation).joinedload(models.Course_Sections.videos)).all()
    course_list = []
    for course in courses:
        sections = []
        for section in course.sectionsRelation:
            videos = []
            for video in section.videos:
                videos.append({
                    "video_id": video.video_id,
                    "video_name": video.video_name,
                    "video_order": video.video_order,
                    "video_text_content": video.video_text_content,
                    "video_url": video.video_url,
                    "duration_sec": video.duration_sec,
                    "created_at": video.created_at,
                    "updated_at": video.updated_at
                })
            sections.append({
                "section_id": section.section_id,
                "section_order": section.section_order,
                "section_name": section.section_name,
                "section_description": section.section_description,
                "videos": videos
            })
        course_list.append({
            "course_id": course.course_id,
            "tutor_id": course.tutor_id,
            "course_name": course.course_name,
            "course_description": course.course_description,
            "level_difficulty": course.level_difficulty,
            "total_duration": course.total_duration,
            "url": course.url,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
            "sections": sections
        })
    return course_list