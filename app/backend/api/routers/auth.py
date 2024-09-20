from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from ...database import get_pg_session
from ...database.crud import users as crud_users
from ..schemas.users import UserCreateSchema, UserSchema
from ..schemas.auth import Token
from ...utils.auth import authenticate_user, create_access_token, get_password_hash


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, db: AsyncSession = Depends(get_pg_session)):
    db_user = await crud_users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    db_user = await crud_users.get_user_by_phone(db, phone=user.phone_number)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already taken")
    user.hashed_password = get_password_hash(user.hashed_password)
    return await crud_users.create_user(db, user=user)


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_pg_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
