import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import PRO_CHANNEL_ID, PRO_CHANNEL_LINK, get_admin_id, router
from subscription_jobs import run_subscription_jobs


async def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN табылмады. .env файлына BOT_TOKEN=... деп жазыңыз.")

    logging.basicConfig(level=logging.INFO)

    if get_admin_id() is None:
        logging.warning(
            "ADMIN_ID .env ішінде жоқ: чектер өңделмейді. "
            "Ботқа /id жазып, өз ID-іңізді алыңыз да, .env-ке ADMIN_ID=... деп жазыңыз."
        )

    if "YOUR_PRIVATE_CHANNEL_LINK" in PRO_CHANNEL_LINK:
        logging.warning("PRO_CHANNEL_LINK әлі нақты сілтемемен ауыстырылмаған (handlers.py)!")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    async def subscription_loop() -> None:
        while True:
            try:
                await run_subscription_jobs(bot, PRO_CHANNEL_ID)
            except Exception:
                logging.exception("Жазылым cron қатесі")
            await asyncio.sleep(60 * 60)

    asyncio.create_task(subscription_loop())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот тоқтатылды")
