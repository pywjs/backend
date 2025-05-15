# scripts/admin.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import asyncio
from core.database import async_session
from apps.users.services import get_user_by_email, create_user
from apps.users.schemas import UserCreate
from core.config import get_settings


async def main():
    settings = get_settings()

    async with async_session() as session:
        user = await get_user_by_email(settings.ADMIN_EMAIL, session)
        if user:
            print(f"✅ Admin {user.email} already exists.")
            return

        user_create = UserCreate(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
        )

        new_user = await create_user(user_create, session)

        new_user.is_admin = True
        new_user.is_staff = True

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        print(f"✅ Admin {new_user.email} created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
