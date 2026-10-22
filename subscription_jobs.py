"""Күнделікті жазылым жұмысы: 24 сағаттық ескерту және мерзімі біткенде шектеу."""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from subscription import due_expirations, due_reminders, mark_expired, mark_reminder_sent

log = logging.getLogger(__name__)

REMINDER_TEXT = (
    "⚠️ Құрметті оқушы! Сіздің GeoHub VIP базаңызды пайдалану мерзімі бітуге жақын "
    "(1 күн қалды). Базаға шектеусіз кіру мүмкіндігін сақтап қалу және жаңартылған "
    "жаңа сұрақтарға доступ алу үшін жазылымды ұзартуды ұмытпаңыз!"
)


async def kick_from_pro_channel(bot: Bot, user_id: int, channel_id: int) -> None:
    """Каналдан шығарады (бан + сразу unban), қайта кіре алмайды сілтемесіз."""
    try:
        await bot.ban_chat_member(channel_id, user_id)
        await bot.unban_chat_member(channel_id, user_id)
    except (TelegramBadRequest, TelegramForbiddenError) as exc:
        log.warning("Каналдан шығару мүмкін болмады user=%s: %s", user_id, exc)


async def run_subscription_jobs(bot: Bot, channel_id: int) -> None:
    for user_id in due_reminders():
        try:
            await bot.send_message(user_id, REMINDER_TEXT)
            mark_reminder_sent(user_id)
            log.info("Ескерту жіберілді: user=%s", user_id)
        except (TelegramBadRequest, TelegramForbiddenError) as exc:
            log.warning("Ескерту жетпеді user=%s: %s", user_id, exc)

    for user_id in due_expirations():
        await kick_from_pro_channel(bot, user_id, channel_id)
        mark_expired(user_id)
        log.info("Жазылым шектелді (expired): user=%s", user_id)
