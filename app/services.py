from typing import Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import ShowUser, UserCreate


async def _create_new_user(body: UserCreate, db_session: AsyncSession) -> ShowUser:
    async with db_session.begin():
        new_user = User(name=body.name)
        db_session.add(new_user)
        await db_session.flush()

        return ShowUser(user_id=new_user.id, name=new_user.name)


async def _get_user_by_id(user_id, db_session: AsyncSession) -> Union[ShowUser, None]:
    async with db_session.begin():
        query = select(User).where(User.id == user_id)
        res = await db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            user = user_row[0]
            return ShowUser(user_id=user.id, name=user.name)
