import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import app.models as models
from app.models import User_Role
from app.database import SessionLocal, engine
from pydantic import BaseModel
from starlette import status
from typing import Optional

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/user_roles',
    tags=['user_roles']
)

class UserRole(BaseModel):
    role_id: int
    role_name: str
    role_description: Optional[str]
    

class UserRoleCreate(BaseModel):
    role_name: str
    role_description: str


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_roles(db: Session = Depends(get_db)):
    user_roles = db.query(User_Role).all()
    user_role_list = []
    for user_role in user_roles:
        user_role_dict = {
            "role_id": user_role.role_id,
            "role_name": user_role.role_name,
            "role_description": user_role.role_description
        }
        user_role_list.append(user_role_dict)
    return user_role_list


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_role(create_user_role: UserRoleCreate, db: Session = Depends(get_db)):
    user_role_model = models.User_Role(
        role_name = create_user_role.role_name, 
        role_description = create_user_role.role_description
    )
    db.add(user_role_model)
    db.commit()
    db.refresh(user_role_model)
    # TODO: CHECK.
    return user_role_model