from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.services.authentication import AuthService
from app.models.schemas.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)
