from datetime import datetime, timedelta

from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_session
from app.models.schemas.users import User, Token, UserCreate
from app.core.settings import settings
from app.db.repositories.users import UserRepository
from app.db.errors import UserDoesNotExist
from app.db import tables

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


async def check_username_is_exist(repo: UserRepository, username: str) -> bool:
    try:
        await repo.get_user_by_username(username=username)
    except UserDoesNotExist:
        return False

    return True


async def check_email_is_exist(repo: UserRepository, email: str) -> bool:
    try:
        await repo.get_user_by_email(email=email)
    except UserDoesNotExist:
        return False

    return True


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()

        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings.jwt_expiration),
            "sub": str(user_data.id),
            "user": user_data.dict()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.repository = UserRepository(session)

    async def register_new_user(self, user_data: UserCreate) -> Token:
        if await check_username_is_exist(self.repository, user_data.username):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="user with this username already exists"
            )

        if await check_email_is_exist(self.repository, user_data.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="user with this email address already exists"
            )

        user = await self.repository.create_user(
            email=user_data.email,
            username=user_data.username,
            password=self.hash_password(user_data.password)
        )
        return self.create_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        wrong_login_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        try:
            user = await self.repository.get_user_by_username(username=username)
        except UserDoesNotExist:
            raise wrong_login_exception

        if not self.verify_password(password, user.password):
            raise wrong_login_exception

        return self.create_token(user)
