import sys
sys.path.append("..")

from typing import List, Union, Optional
import app.models as models
# from app.models import Tags, Tag_Type_Enum, Centers_Enum, Studies_Enum, Subjects_Enum, Grades_Enum
from app.models import Tag_Type_Enum, Tag

from pydantic import BaseModel
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

# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

router = APIRouter(
    prefix='/tags',
    tags=['tags']
)


# class CenterCreate(BaseModel):
#     center: Centers_Enum

# class StudyCreate(BaseModel):
#     study: Studies_Enum

# class SubjectCreate(BaseModel):
#     subject: Subjects_Enum

# class GradeCreate(BaseModel):
#     grade: Grades_Enum
    
#  TODO. check duplicity in all these classes
# class CenterCreate(BaseModel):
#     center_id: int
#     center: Centers_Enum

# class StudyCreate(BaseModel):
#     study_id: int
#     study: Studies_Enum

# class SubjectCreate(BaseModel):
#     subject_id: int
#     subject: Subjects_Enum

# class GradeCreate(BaseModel):
#     grade_id: int
#     grade: Grades_Enum


# POST endpoints for creating each tag type

class TagCreate(BaseModel):
    tag_type: Tag_Type_Enum
    name: str

@router.post('/tag', status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    existing_tag = db.query(Tag).filter(Tag.tag_type == tag.tag_type, Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = Tag(tag_type=tag.tag_type, name=tag.name)
    db.add(new_tag)
    db.commit()
    return {"message": "Tag created successfully", "tag_id": new_tag.id}


@router.get('/', response_model=List[TagCreate])
async def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [{"tag_id": tag.id, "tag_type": tag.tag_type, "name": tag.name} for tag in tags]

# @router.post('/centers', status_code=status.HTTP_201_CREATED)
# async def create_center(tag: CenterCreate, db: Session = Depends(get_db)):
#     center = db.query(Center).filter(Center.center == tag.center).first()
#     if center:
#         raise HTTPException(status_code=400, detail="Center already exists")
    
#     new_center = Center(center=tag.center)
#     db.add(new_center)
#     db.commit()
#     return {"message": "Center created successfully", "center_id": new_center.center_id}

# @router.post('/studies', status_code=status.HTTP_201_CREATED)
# async def create_study(tag: StudyCreate, db: Session = Depends(get_db)):
#     study = db.query(Study).filter(Study.study == tag.study).first()
#     if study:
#         raise HTTPException(status_code=400, detail="Study already exists")
    
#     new_study = Study(study=tag.study)
#     db.add(new_study)
#     db.commit()
#     return {"message": "Study created successfully", "study_id": new_study.study_id}

# @router.post('/subjects', status_code=status.HTTP_201_CREATED)
# async def create_subject(tag: SubjectCreate, db: Session = Depends(get_db)):
#     subject = db.query(Subject).filter(Subject.subject == tag.subject).first()
#     if subject:
#         raise HTTPException(status_code=400, detail="Subject already exists")
    
#     new_subject = Subject(subject=tag.subject)
#     db.add(new_subject)
#     db.commit()
#     return {"message": "Subject created successfully", "subject_id": new_subject.subject_id}

# @router.post('/grades', status_code=status.HTTP_201_CREATED)
# async def create_grade(tag: GradeCreate, db: Session = Depends(get_db)):
#     grade = db.query(Grade).filter(Grade.grade == tag.grade).first()
#     if grade:
#         raise HTTPException(status_code=400, detail="Grade already exists")
    
#     new_grade = Grade(grade=tag.grade)
#     db.add(new_grade)
#     db.commit()
#     return {"message": "Grade created successfully", "grade_id": new_grade.grade_id}

# GET endpoints for retrieving all tags

# @router.get('/centers', response_model=List[CenterCreate])
# async def get_centers(db: Session = Depends(get_db)):
#     centers = db.query(Center).all()
#     return [{"center_id": center.center_id, "center": center.center} for center in centers]

# @router.get('/studies', response_model=List[StudyCreate])
# async def get_studies(db: Session = Depends(get_db)):
#     studies = db.query(Study).all()
#     return [{"study_id": study.study_id, "study": study.study} for study in studies]

# @router.get('/subjects', response_model=List[SubjectCreate])
# async def get_subjects(db: Session = Depends(get_db)):
#     subjects = db.query(Subject).all()
#     return [{"subject_id": subject.subject_id, "subject": subject.subject} for subject in subjects]

# @router.get('/grades', response_model=List[GradeCreate])
# async def get_grades(db: Session = Depends(get_db)):
#     grades = db.query(Grade).all()
#     return [{"grade_id": grade.grade_id, "grade": grade.grade} for grade in grades]


# class TagBase(BaseModel):
#     tag_type_enum: Tag_Type_Enum

# class TagCenter(TagBase):
#     centers_enum: Centers_Enum

# class TagStudy(TagBase):
#     studies_enum: Studies_Enum

# class TagSubject(TagBase):
#     subjects_enum: Subjects_Enum

# class TagGrade(TagBase):
#     grades_enum: Grades_Enum

# class TagInDB(BaseModel):
#     tag_id: int
#     tag_type_enum: Tag_Type_Enum
#     centers_enum: Optional[Centers_Enum]
#     studies_enum: Optional[Studies_Enum]
#     subjects_enum: Optional[Subjects_Enum]
#     grades_enum: Optional[Grades_Enum]

# @router.get('/', status_code=status.HTTP_200_OK)
# async def get_tags(db: Session = Depends(get_db)):
#     tags = db.query(Tag).all()
#     tag_list = []
#     for tag in tags:
#         tag_dict = {
#             "tag_id": tag.tag_id,
#             "tag_type_enum": tag.tag_type_enum,
#             "centers_enum": tag.centers_enum,
#             "studies_enum": tag.studies_enum,
#             "subjects_enum": tag.subjects_enum,
#             "grades_enum": tag.grades_enum,
#         }
#         tag_list.append(tag_dict)
#     return tag_list

# CreateTag = Union[TagCenter, TagStudy, TagSubject, TagGrade]

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_tag(tag: CreateTag, db: Session = Depends(get_db)):
#     new_tag = Tag(
#         tag_type_enum=tag.tag_type_enum,
#         centers_enum=getattr(tag, 'centers_enum', None),
#         studies_enum=getattr(tag, 'studies_enum', None),
#         subjects_enum=getattr(tag, 'subjects_enum', None),
#         grades_enum=getattr(tag, 'grades_enum', None),
#     )

#     db.add(new_tag)
#     db.commit()

#     return {"message": "Tag created successfully", "tag_id": new_tag.tag_id}
