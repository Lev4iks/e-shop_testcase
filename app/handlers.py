from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import ShowUser
from app.schemas import UserCreate
from app.services import _create_new_user, _get_user_by_id
from app.database import get_db_session

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db_session: AsyncSession = Depends(get_db_session)) -> ShowUser:
    try:
        return await _create_new_user(body, db_session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id, db_session: AsyncSession = Depends(get_db_session)) -> ShowUser:
    user = await _get_user_by_id(user_id, db_session)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user
