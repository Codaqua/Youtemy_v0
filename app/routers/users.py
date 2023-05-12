import sys
sys.path.append("..")

from datetime import datetime
from typing import Optional, List, Annotated
import app.models as models
from app.models import Users, User_Role, Role_Permission, Permission

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

# from ..database import get_db
# from app.utils.security import get_current_user
from app.database import SessionLocal, engine
# from .auth import get_current_user
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/users',
    tags=['users']
    # TODO : check vi135 -> responses= {404: {"description": "Not found"}}
)

# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(BaseModel):
    user_id: int
    username: str
    name: str
    surname: str
    email: str
    avatar_image: Optional[str] = None
    hashed_password: str
    # created_at: str
    # updated_at: str
    role_id: int
    # role_id: Optional[int] = None
    # TODO: PENDIENTE
    
# @router.get("/")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Users).all()


# @router.get('/', response_model=List[User], status_code=status.HTTP_200_OK)
# async def get_user(db: Session = Depends(get_db)):

#     return db.query(models.Users).all()

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    user_list = []
    for user in users:
        user_dict = {
            "user_id": user.user_id,
            "username": user.username,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "avatar_image": user.avatar_image,
            "hashed_password": user.hashed_password
        }
        user_list.append(user_dict)
    return user_list



# @router.post("/")
# async def create_user(user: User, db: Session = Depends(get_db)):
#     # role = db.query(Role).filter(Role.role_id == user.role_id).first()
#     # if not role:
#     #     raise HTTPException(status_code=400, detail="Invalid role_id")
    
#     user_model = models.Users()
#     user_model.username = user.username
#     user_model.name = user.name
#     user_model.surname = user.surname
#     # user_model.password = bcrypt_context.hash(user.password)
#     user_model.email = user.email
#     user_model.avatar_image = user.avatar_image
#     # user_model.role_id = user.role_id
#     # TODO: PENDIENTE

#     db.add(user_model)
#     db.commit()

#     return {"message": "User created successfully", "user_id": user_model.user_id}


# @router.get('/', status_code=status.HTTP_200_OK)
# async def get_user(users: user_dependency, db: db_dependency):
#     if Users is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return db.query(Users).filter(Users.user_id == users.get('id')).first()


# @router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
# async def change_password(users: user_dependency, db: db_dependency,
#                           user_verification: UserVerification):
#     if users is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     user_model = db.query(Users).filter(Users.user_id == users.get('id')).first()

#     if not bcrypt_context.verify(user_verification.password, user_model.password):
#         raise HTTPException(status_code=401, detail='Error on password change')
#     user_model.password = bcrypt_context.hash(user_verification.new_password)
#     db.add(user_model)
#     db.commit()

