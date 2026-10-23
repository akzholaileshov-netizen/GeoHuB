import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import PRO_CHANNEL_ID, PRO_CHANNEL_LINK, get_admin_id, router
from subscription_jobs import run_subscription_jobs

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")


async def start_health_server() -> None:
    """Render Web Service $PORT ашпаса, 'No open HTTP ports' деп өшеді."""
    port = os.getenv("PORT")
    if not port:
        return

    from aiohttp import web

    async def ok(_request: web.Request) -> web.Response:
        return web.Response(text="GeoHub ok")

    app = web.Application()
    app.router.add_get("/", ok)
    app.router.add_get("/health", ok)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(port)).start()
    logging.info("Health server 0.0.0.0:%s", port)


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN табылмады. Жергілікті .env немесе Render Environment-қа BOT_TOKEN қойыңыз."
        )

    logging.basicConfig(level=logging.INFO)

    if get_admin_id() is None:
        logging.warning(
            "ADMIN_ID жоқ: чектер өңделмейді. "
            "Ботқа /id жазып, ADMIN_ID-ді Environment-қа қойыңыз."
        )

    if "YOUR_PRIVATE_CHANNEL_LINK" in PRO_CHANNEL_LINK:
        logging.warning("PRO_CHANNEL_LINK әлі нақты сілтемемен ауыстырылмаған (handlers.py)!")

    await start_health_server()

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
