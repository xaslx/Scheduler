from datetime import datetime, timedelta
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Request,
    Body,
    Form,
    status,
)
from app.auth.dependencies import get_all_notifications
from app.schemas.notification_schemas import NotificationOut
from app.utils.current_time import current_time
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.schemas.user_schema import UserRegister, UserOut, UserLogin
from app.repository.user_repo import UserRepository
from app.models.user_model import User
from exceptions import UserAlreadyExistsException, UserNotFound
from app.auth.auth import authenticate_user, get_password_hash, create_access_token
import secrets
from app.utils.templating import templates
from typing import Annotated
from fastapi.responses import HTMLResponse, JSONResponse
from app.tasks.tasks import register_confirmation_message


auth_router: APIRouter = APIRouter(
    prefix="/auth", tags=["Аутентификация и Авторизация"]
)


@auth_router.get("/register", status_code=200)
async def get_register_template(
    request: Request,
    user: User = Depends(get_current_user),
    notifications: list[NotificationOut] = Depends(get_all_notifications),
) -> HTMLResponse:
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "user": user, "notifications": notifications},
    )


@auth_router.post("/register", status_code=201)
async def rigister_user(
    user: UserRegister, session: AsyncSession = Depends(get_async_session)
):
    exist_user: User = await UserRepository.find_one_or_none(
        session=session, email=user.email
    )
    if exist_user:
        raise UserAlreadyExistsException

    hashed_password: str = get_password_hash(user.password)
    new_personal_link: str = secrets.token_hex(8)
    new_user: User = await UserRepository.add(
        session=session,
        **user.model_dump(exclude="password"),
        personal_link=new_personal_link,
        hashed_password=hashed_password,
    )
    register_confirmation_message.delay(email_to=user.email)
    return new_user


@auth_router.get("/after_register", status_code=200)
async def after_register_template(
    request: Request,
    user: User = Depends(get_current_user),
    notifications: list[NotificationOut] = Depends(get_all_notifications),
) -> HTMLResponse:
    return templates.TemplateResponse(
        "after_register.html",
        {"request": request, "user": user, "notifications": notifications},
    )


@auth_router.post("/login", status_code=200)
async def login_user(
    response: Response,
    user: UserLogin,
    session: AsyncSession = Depends(get_async_session),
) -> str:
    user = await authenticate_user(user.email, user.password, async_db=session)
    if not user:
        raise UserNotFound

    access_token, expire = create_access_token({"sub": str(user.id)})
    max_age = (expire - datetime.utcnow()).total_seconds()

    response.set_cookie(
        "user_access_token", access_token, httponly=True, max_age=max_age
    )
    return access_token


@auth_router.get("/login", status_code=200)
async def get_login_template(
    request: Request, user: User = Depends(get_current_user)
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="login.html", context={"user": user}
    )


@auth_router.post("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
