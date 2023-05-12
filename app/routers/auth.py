import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional

# Library for encrypting passwords
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError



from typing import Optional, List
from fastapi import Depends, APIRouter
import app.models as models
from app.models import Users
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

# from ..database import get_db
# from app.utils.security import get_current_user
from app.database import SessionLocal, engine
# from .auth import get_current_user
from passlib.context import CryptContext

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engine)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


class CreateUserRequest(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    avatar_image: Optional[str] = None
    password: str
    role_id: int
    # created_at: str
    # updated_at: str
    # TODO: PENDIENTE


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users)\
        .filter(models.Users.username == username)\
        .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    # role = db.query(Role).filter(Role.role_id == user.role_id).first()
    # if not role:
    #     raise HTTPException(status_code=400, detail="Invalid role_id")
    create_user_model = Users(
        username = create_user_request.username,
        name = create_user_request.name,
        surname = create_user_request.surname,
        email = create_user_request.email,
        avatar_image = create_user_request.avatar_image,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role_id = create_user_request.role_id,
        # TODO: PENDIENTE
    )

    db.add(create_user_model)
    db.commit()
    # TODO : vi136. db.flush()

    return {"message": "User created successfully", "user_id": create_user_model.user_id}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.user_id,
                                expires_delta=token_expires)
    return {"token": token}


#Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response





# @router.post("/create/user")
# async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
#     create_user_model = models.Users()
#     create_user_model.email = create_user.email
#     create_user_model.username = create_user.username
#     create_user_model.first_name = create_user.first_name
#     create_user_model.last_name = create_user.last_name

#     hash_password = get_password_hash(create_user.password)

#     create_user_model.hashed_password = hash_password
#     create_user_model.is_active = True

#     db.add(create_user_model)
#     db.commit()







