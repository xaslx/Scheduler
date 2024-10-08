from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.notification_repo import NotificationRepository
from app.schemas.notification_schemas import NotificationOut
from logger import logger
from redis_init import redis


async def get_notifications(session: AsyncSession):
    cached_data = await redis.hgetall("notifications")
    if not cached_data:
        notifications: list[NotificationOut] = (
            await NotificationRepository.find_all_notif(session=session)
        )
        notifications_out = [
            NotificationOut.model_validate(notif) for notif in notifications
        ]
        for notification in notifications_out:
            await redis.hset(
                "notifications", notification.id, notification.model_dump_json()
            )
            await redis.expire("notifications", 600)
    else:
        notifications: list[NotificationOut] = sorted(
            [
                NotificationOut.model_validate_json(value)
                for value in cached_data.values()
            ],
            key=lambda notif: notif.created_at,
            reverse=True,
        )
    return notifications


async def delete_cache_personal_link(personal_link: str):
    try:
        await redis.delete(personal_link)
    except:
        logger.error("Ошибка при удалении кэша")


async def delete_cache_notifications():
    try:
        await redis.delete("notifications", "all_notifications")
    except:
        logger.error("Ошибка при удалении кэша")
