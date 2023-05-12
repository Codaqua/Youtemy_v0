from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import UniqueConstraint
import enum

# class Authentication(Base):
    # __tablename__ = "user_authentication"

    # role_id = Column(Integer, primary_key=True, index=True)
    # role_name = Column(String(50), unique=True, nullable=False)
    # role_description = Column(Text)
#   TODO: PENDIENTE



class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    hashed_password  = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    avatar_image = Column(String(255))
    # created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    # updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    # TODO: PENDIENTE
    role_id = Column(Integer, ForeignKey("user_roles.role_id"), nullable=False)
    # TODO: role_id = Column(Integer, ForeignKey("user_roles.role_id"), nullable=False, default=1)
    # TODO : role_id = Column(Integer, ForeignKey("user_roles.role_id"), nullable=False, server_default=RoleType.student.name)
    
    # role_id = Column(Integer, ForeignKey("roles.role_id"))

    # role = relationship("Role", back_populates="users")
    # TODO: PENDIENTE
    # courses = relationship("Course", back_populates="creator")

class User_Role(Base):  
    __tablename__ = "user_roles"

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)
    role_description = Column(Text)
# TODO: esto podría ser un enum

    # users = relationship("Users", back_populates="role")
    # TODO: PENDIENTE

class Role_Permission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, primary_key=True)
    role_permission_id = Column(Integer, ForeignKey("user_roles.role_id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.permission_id"), nullable=False)
        # TODO: PENDIENTE


class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String(50), unique=True, nullable=False)
    permission_description = Column(Text)
    # created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    # updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
    # TODO: PENDIENTE



#  ////////////////////////////////////////////////////////////

class Course_Enrolled(Base):
    __tablename__ = 'courses_enrolled'
    
    enrolled_courses_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    progression_status = Column(Float)
    created_at = Column(TIMESTAMP, default=func.now())


class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    course_name = Column(String(50), nullable=False)
    course_description = Column(String(255))
    level_difficulty = Column(Integer)
    total_duration = Column(Integer)
    url = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP)

    # Relationship with Course_Sections
    sectionsRelation = relationship("Course_Sections", back_populates="course")
    course_sections = relationship("Course_Sections", back_populates="course")
    course_keywords = relationship("Course_Keyword", back_populates="course")
    course_tags = relationship("Course_Tag", back_populates="course")
    # tutor_id = relationship("Users", back_populates="courses")
    # TODO: PENDIENTE


class Course_Sections(Base):
    __tablename__ = 'course_sections'
    
    section_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    section_order = Column(Integer)
    section_name = Column(String(50), nullable=False)
    section_description = Column(String(255))
    
    # course = relationship("Course", back_populates="course_sections")
    
    # course = relationship("Course", back_populates="sections")
        
    # relationship with Course
    course = relationship("Course", back_populates="course_sections")
    course = relationship("Course", back_populates="sectionsRelation")
    # relationship with Video
    videos = relationship("Video", back_populates="sectionsRelation")

class Video(Base):
    __tablename__ = "videos"

    video_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey('course_sections.section_id'), nullable=False)
    video_name = Column(String(50), nullable=False)
    video_order = Column(Integer)
    video_text_content = Column(Text)
    video_url = Column(String(100))
    duration_sec = Column(Integer)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP)    

    # relationship with Course_Sections
    sectionsRelation = relationship("Course_Sections", back_populates="videos")  

class Tag_Type_Enum(enum.Enum):
    centers = "Centers"
    studies = "Studies"
    subjects = "Subjects"
    grades = "Grades"

# class Centers_Enum(enum.Enum):
#     uoc = "Universitat Oberta de Catalunya"
#     upm = "Universidad Politécnica de Madrid"
#     uo = "Universidad de Oviedo"

# class Studies_Enum(enum.Enum):
#     computer = "Computer Engineering"
#     economics = "Economics"
#     law = "Law"

# class Subjects_Enum(enum.Enum):
#     algebra = "Algebra"
#     maths = "Mathematics"
#     statistics = "Statistics"

# class Grades_Enum(enum.Enum):
#     grade_1 = "1"
#     grade_2 = "2"
#     grade_3 = "3"
#     grade_4 = "4"

# class Tag(Base):
#     __tablename__ = 'tags'
    
#     tag_id = Column(Integer, primary_key=True)
#     tag_type_enum = Column(Enum(Tag_Type_Enum))
#     centers_enum = Column(Enum(Centers_Enum))
#     studies_enum = Column(Enum(Studies_Enum))
#     subjects_enum = Column(Enum(Subjects_Enum))
#     grades_enum = Column(Enum(Grades_Enum))
    # tag_name = Column(String(50), unique=True)
    # tag_description = Column(String(100))

# class Tag(Base):
#     __tablename__ = 'tags'
#     tag_id = Column(Integer, primary_key=True)
#     tag_type = Column(Enum(Tag_Type_Enum), nullable=False)
#     name = Column(String, nullable=False, unique=True)

#     course_tags = relationship("Course_Tag", back_populates="tag")

# class Center(Base):
#     __tablename__ = 'centers'
#     center_id = Column(Integer, primary_key=True)
#     center = Column(Enum(Centers_Enum), unique=True)
    
#     course_tags = relationship("Course_Tag", back_populates="center")

# class Study(Base):
#     __tablename__ = 'studies'
#     study_id = Column(Integer, primary_key=True)
#     study = Column(Enum(Studies_Enum), unique=True)
    
#     course_tags = relationship("Course_Tag", back_populates="study")

# class Subject(Base):
#     __tablename__ = 'subjects'
#     subject_id = Column(Integer, primary_key=True)
#     subject = Column(Enum(Subjects_Enum), unique=True)
    
#     course_tags = relationship("Course_Tag", back_populates="subject")

# class Grade(Base):
#     __tablename__ = 'grades'
#     grade_id = Column(Integer, primary_key=True)
#     grade = Column(Enum(Grades_Enum), unique=True)
    
#     course_tags = relationship("Course_Tag", back_populates="grade")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_type = Column(Enum(Tag_Type_Enum), nullable=False)
    name = Column(String, nullable=False, unique=True)

    course_tags = relationship("Course_Tag", back_populates="tag")

class Course_Tag(Base):
    __tablename__ = 'course_tags'
    course_tag_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    # center_id = Column(Integer, ForeignKey('centers.center_id'), nullable=True)
    # study_id = Column(Integer, ForeignKey('studies.study_id'), nullable=True)
    # subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=True)
    # grade_id = Column(Integer, ForeignKey('grades.grade_id'), nullable=True)

    course = relationship("Course", back_populates="course_tags")
    tag = relationship("Tag", back_populates="course_tags")
    # center = relationship("Center", back_populates="course_tags")
    # study = relationship("Study", back_populates="course_tags")
    # subject = relationship("Subject", back_populates="course_tags")
    # grade = relationship("Grade", back_populates="course_tags")
    
# class Course_Tag(Base):
#     __tablename__ = 'course_tags'
    
#     course_tag_id = Column(Integer, primary_key=True)
#     course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
#     tag_id = Column(Integer, ForeignKey('tags.tag_id'), nullable=False)

class Course_Keyword(Base):
    __tablename__ = 'course_keywords'
    
    keyword_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    keyword_name = Column(String(50), nullable=False)
    keyword_description = Column(String(100), unique=True)
    
    course = relationship("Course", back_populates="course_keywords")

