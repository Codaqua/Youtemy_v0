import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import app.models as models
from app.models import Permission, User_Role, Role_Permission
from app.database import SessionLocal, engine
from pydantic import BaseModel
from starlette import status

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/role_permissions',
    tags=['role_permissions']
)

class RolePermission(BaseModel):
    role_id: int
    role_permission_id: int
    permission_id: int


class RolePermissionCreate(BaseModel):
    role_permission_id: int
    permission_id: int


@router.get('/', status_code=status.HTTP_200_OK)
async def get_role_permissions(db: Session = Depends(get_db)):
    role_permissions = db.query(Role_Permission).all()
    role_permission_list = []
    for role_permission in role_permissions:
        role_permission_dict = {
            "role_id": role_permission.role_id,
            "role_permission_id": role_permission.role_permission_id,
            "permission_id": role_permission.permission_id
        }
        role_permission_list.append(role_permission_dict)
    return role_permission_list


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_role_permission(create_role_permission: RolePermissionCreate, db: Session = Depends(get_db)):
    role_permission_model = models.Role_Permission(
        role_permission_id=create_role_permission.role_permission_id, 
        permission_id=create_role_permission.permission_id
    )
    
    db.add(role_permission_model)
    db.commit()
    db.refresh(role_permission_model)
    # TODO: CHECK.
    return role_permission_model