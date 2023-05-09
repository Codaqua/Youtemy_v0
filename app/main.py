from fastapi import FastAPI
# from app.env import config
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import declarative_base
from app.database import engine, SessionLocal, Base
import app.models as models
from app.routers import users, auth, permission, role_permission, user_roles, course, course_enrolled, course_keyword, course_section, course_tag, tag, video
# , courses, sections, videos, authentication, roles, permissions


# MODE = config("MODE", cast=str, default="defecto")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Jason
# @app.get("/")
# def home_page():
#     return {"Hello": "World", "mode": MODE}


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(course_enrolled.router)
app.include_router(course_keyword.router)
app.include_router(course_section.router)
app.include_router(course_tag.router)
app.include_router(permission.router)
app.include_router(role_permission.router)
app.include_router(tag.router)
app.include_router(user_roles.router)
app.include_router(video.router)







