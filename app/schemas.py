# from typing import List, Optional
# from pydantic import BaseModel
# from app.models import Course

# # TODO : Verify if this file is still needed

# class VideoSchema(BaseModel):
#     video_id: int
#     video_name: str
#     video_order: int
#     video_text_content: str
#     video_url: str
#     duration_sec: int

#     class Config:
#         orm_mode = True


# class CourseSectionSchema(BaseModel):
#     section_id: int
#     section_order: int
#     section_name: str
#     section_description: str
#     videos: List[VideoSchema]

#     class Config:
#         orm_mode = True


# class CourseKeywordSchema(BaseModel):
#     keyword_id: int
#     keyword_name: str
#     keyword_description: str

#     class Config:
#         orm_mode = True


# class CenterSchema(BaseModel):
#     center_id: int
#     center: Centers_Enum

#     class Config:
#         orm_mode = True

# class StudySchema(BaseModel):
#     study_id: int
#     study: Studies_Enum

#     class Config:
#         orm_mode = True

# class SubjectSchema(BaseModel):
#     subject_id: int
#     subject: Subjects_Enum

#     class Config:
#         orm_mode = True

# class GradeSchema(BaseModel):
#     grade_id: int
#     grade: Grades_Enum

#     class Config:
#         orm_mode = True


# class CourseTagSchema(BaseModel):
#     course_tag_id: int
#     course_id: int
#     center_id: Optional[int] = None
#     study_id: Optional[int] = None
#     subject_id: Optional[int] = None
#     grade_id: Optional[int] = None
#     center: Optional[CenterSchema] = None
#     study: Optional[StudySchema] = None
#     subject: Optional[SubjectSchema] = None
#     grade: Optional[GradeSchema] = None

#     class Config:
#         orm_mode = True


# class CourseWithDetails(BaseModel):
#     course_id: int
#     course_name: str
#     course_description: str
#     level_difficulty: int
#     course_sections: List[CourseSectionSchema]
#     course_keywords: List[CourseKeywordSchema]
#     course_tags: List[CourseTagSchema]

#     class Config:
#         orm_mode = True

# # class CourseWithDetails(Course):
# #     course_sections: List[CourseSectionSchema] = []
# #     course_keywords: List[CourseKeywordSchema] = []
# #     course_tags: List[CourseTagSchema] = []

# #     class Config:
# #         orm_mode = True

# # class TagSchema(BaseModel):
# #     tag_id: int
# #     tag_type_enum: Tag_Type_Enum
# #     centers_enum: Optional[Centers_Enum] = None
# #     studies_enum: Optional[Studies_Enum] = None
# #     subjects_enum: Optional[Subjects_Enum] = None
# #     grades_enum: Optional[Grades_Enum] = None

# #     class Config:
# #         orm_mode = True