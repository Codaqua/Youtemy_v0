import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import app.models as models
from app.models import Permission
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
    prefix='/permissions',
    tags=['permissions']
)

class PermissionModel(BaseModel):
    permission_id: int
    permission_name: str
    permission_description: Optional[str]
    # created_at: datetime
    # updated_at: datetime


class PermissionCreate(BaseModel):
    permission_name: str
    permission_description: str


@router.get('/', status_code=status.HTTP_200_OK)
async def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    permission_list = []
    for permission in permissions:
        permission_dict = {
            "permission_id": permission.permission_id,
            "permission_name": permission.permission_name,
            "permission_description": permission.permission_description,
            # "created_at": permission.created_at,
            # "updated_at": permission.updated_at
        }
        permission_list.append(permission_dict)
    return permission_list


@router.post("/", status_code=201)
async def create_permission(create_permission: PermissionCreate, db: Session = Depends(get_db)):
    create_permission_model = models.Permission(
        permission_name=create_permission.permission_name, 
        permission_description=create_permission.permission_description
    )
    db.add(create_permission_model)
    db.commit()
    db.refresh(create_permission_model)
    # TODO: Check.
    return create_permission_model