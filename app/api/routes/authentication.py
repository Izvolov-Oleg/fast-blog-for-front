from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.services.authentication import AuthService
from app.models.schemas.users import (
    UserCreate,
    Token
)

router = APIRouter()


@router.post('/sign-up', response_model=Token)
async def sign_up(user_data: UserCreate,
                  service: AuthService = Depends()):
    return await service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(),
                  service: AuthService = Depends()):
    return await service.authenticate_user(
        form_data.username,
        form_data.password
    )

