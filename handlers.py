import asyncio
import html
import logging
import os
from datetime import timedelta

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, ChatMemberUpdated, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from keyboards import (
    CB_BACK_TO_MAIN,
    CB_BACK_TO_NOMENCLATURE,
    CB_CONTINENTS,
    CB_FULL_BASE,
    CB_BACK_TO_GRADES,
    CB_GEO_7,
    CB_GEO_8,
    CB_GEO_9,
    CB_GRADE_10_11,
    CB_I_PAID,
    CB_NOMENCLATURE,
    CB_OCEANS,
    CB_PLACEMENT_TEST,
    CB_PAY_NO,
    CB_PAY_OK,
    CB_PRO_BACK_TO_PAY,
    CB_PRO_INFO,
    CB_PRO_LEVEL,
    CB_QUIZZES,
    MAIN_MENU_BUTTONS,
    admin_review_kb,
    continents_kb,
    full_base_kb,
    geo_7_kb,
    geo_8_kb,
    geo_9_kb,
    main_menu_kb,
    nomenclature_kb,
    oceans_kb,
    placement_test_kb,
    pro_info_kb,
    pro_invite_kb,
    pro_payment_kb,
    pro_upgrade_kb,
)

router = Router()

CONFETTI_EFFECT_ID = "5046509860389126442"  # 🎉 Telegram хабарлама эффектісі

# 1-кезең: жүктелу кадрлары (глобус айналады, пайыз өседі)
LOADING_FRAMES = (
    "🌍 <b>GeoHub</b>\n\n▰▰▱▱▱▱▱▱▱▱  <b>20%</b>\n<i>Карталар жүктелуде...</i>",
    "🌎 <b>GeoHub</b>\n\n▰▰▰▰▱▱▱▱▱▱  <b>40%</b>\n<i>Материалдар жиналуда...</i>",
    "🌏 <b>GeoHub</b>\n\n▰▰▰▰▰▰▰▰▱▱  <b>80%</b>\n<i>Тесттер дайындалуда...</i>",
    "🌍 <b>GeoHub</b>\n\n▰▰▰▰▰▰▰▰▰▰  <b>100%</b>\n✅ <i>Дайын!</i>",
)

WELCOME_TEXT = (
    "🌍 <b>GeoHub-қа қош келдің!</b>\n\n"
    "Географияны бірге үйренеміз 🚀\n"
    "Төменнен бөлімді таңда 👇"
)

FRAME_DELAY = 0.7  # кадрлар арасындағы кідіріс (сек)
BUTTON_DELAY = 0.35  # батырмалар бірінен соң бірі ашылу кідірісі (сек)


async def safe_edit(message: Message, text: str) -> None:
    try:
        await message.edit_text(text)
    except TelegramBadRequest:
        pass  # мәтін өзгермесе немесе Telegram бас тартса, жалғастыра береміз


async def play_loading(message: Message) -> None:
    """1) Динамикалық жүктелу: 20% -> 40% -> 80% -> 100%."""
    loader = await message.answer("🌍 <b>GeoHub</b>\n\n▱▱▱▱▱▱▱▱▱▱  <b>0%</b>")
    for frame in LOADING_FRAMES:
        await asyncio.sleep(FRAME_DELAY)
        await safe_edit(loader, frame)
    await asyncio.sleep(FRAME_DELAY)
    await loader.delete()


async def play_celebration(message: Message) -> None:
    """2) Мерекелік эмодзи: жалғыз эмодзи Telegram-да үлкен анимациямен ойнайды."""
    party = await message.answer("🎉")
    await asyncio.sleep(1.6)
    await party.delete()


async def reveal_menu(message: Message) -> None:
    """3) Мәзір конфетти эффектісімен шығады, батырмалар бірден-бірден ашылады."""
    try:
        menu = await message.answer(
            WELCOME_TEXT,
            reply_markup=main_menu_kb(visible=1),
            message_effect_id=CONFETTI_EFFECT_ID,
        )
    except TelegramBadRequest:
        # Эффект қолдау таппаса, эффектісіз жібереміз
        menu = await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(visible=1))

    for count in range(2, len(MAIN_MENU_BUTTONS) + 1):
        await asyncio.sleep(BUTTON_DELAY)
        try:
            await menu.edit_reply_markup(reply_markup=main_menu_kb(visible=count))
        except TelegramBadRequest:
            pass


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Ескі пернетақта (reply keyboard) қалып қойса, оны жою
    cleanup = await message.answer("…", reply_markup=ReplyKeyboardRemove())
    await cleanup.delete()

    await play_loading(message)      # 1) жүктелу анимациясы
    await play_celebration(message)  # 2) мерекелік эмодзи
    await reveal_menu(message)       # 3) конфетти + мәзір ашылуы


# Әр хэндлерде callback.answer() мәтінсіз шақырылады: ол тек батырмадағы
# "жүктелу" индикаторын өшіреді, пайдаланушыға ештеңе көрсетпейді.


async def show_menu(callback: CallbackQuery, keyboard: InlineKeyboardMarkup) -> None:
    """Хабарлама мәтінін өзгертпей, тек астындағы батырмаларды ауыстырады."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        except TelegramBadRequest:
            pass  # батырмалар бұрыннан осындай болса, ештеңе істемейміз


# --- Навигация (мәзірден мәзірге ауысу) ---


@router.callback_query(F.data == CB_FULL_BASE)
async def full_base_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, full_base_kb())  # 7, 8, 9 сынып


@router.callback_query(F.data == CB_NOMENCLATURE)
async def nomenclature_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, nomenclature_kb())  # Материктер, Мұхиттар


@router.callback_query(F.data == CB_CONTINENTS)
async def continents_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, continents_kb())


@router.callback_query(F.data == CB_OCEANS)
async def oceans_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, oceans_kb())


@router.callback_query(F.data == CB_BACK_TO_MAIN)
async def back_to_main_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    # Мәтінді де қайтарамыз (PRO бөлімінен оралғанда мәтін өзгеріп кеткен болады)
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_kb())
        except TelegramBadRequest:
            pass


@router.callback_query(F.data == CB_BACK_TO_NOMENCLATURE)
async def back_to_nomenclature_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, nomenclature_kb())


# --- Материктер (бос хэндлерлер) ---


# "Еуразия" — URL-батырма (Google Drive), хэндлер қажет емес. Сілтеме: keyboards.py → EURASIA_URL


# "Солтүстік Америка" — URL-батырма (Google Drive), хэндлер қажет емес.
# Сілтеме: keyboards.py → NORTH_AMERICA_URL


# "Африка" — URL-батырма (Google Drive), хэндлер қажет емес. Сілтеме: keyboards.py → AFRICA_URL


# "Оңтүстік Америка" — URL-батырма (Google Drive), хэндлер қажет емес.
# Сілтеме: keyboards.py → SOUTH_AMERICA_URL


# "Антарктида" — URL-батырма (Google Drive), хэндлер қажет емес.
# Сілтеме: keyboards.py → ANTARCTICA_URL


# "Австралия" — URL-батырма (Google Drive), хэндлер қажет емес.
# Сілтеме: keyboards.py → AUSTRALIA_URL
# Барлық 6 материк — URL-батырма, сондықтан материктерге callback-хэндлер жоқ.


# --- Мұхиттар ---
# Барлық 4 мұхит (Тынық, Атлант, Үнді, Солтүстік Мұзды) — URL-батырма (Google Drive),
# сондықтан callback-хэндлер қажет емес. Сілтемелер keyboards.py ішінде
# (PACIFIC_URL, ATLANTIC_URL, INDIAN_URL, ARCTIC_URL).


# --- "Толық база" ішкі бөлімдері (бос хэндлерлер) ---


GEO_7_TEXT = "🌐 <b>7 сынып география — тақырыпты таңдаңыз:</b>"
GEO_8_TEXT = "🌏 <b>8 сынып география — тақырыпты таңдаңыз:</b>"
GEO_9_TEXT = "🌐 <b>9 сынып география — тақырыпты таңдаңыз:</b>"


@router.callback_query(F.data == CB_GEO_7)
async def geo_7_handler(callback: CallbackQuery) -> None:
    """"7 сынып география": сол хабарлама тақырыптар тізіміне ауысады."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(GEO_7_TEXT, reply_markup=geo_7_kb())
        except TelegramBadRequest:
            pass


@router.callback_query(F.data == CB_BACK_TO_GRADES)
async def back_to_grades_handler(callback: CallbackQuery) -> None:
    """"⬅️ Артқа": 7/8/9 сынып таңдауына қайтады (басты мәзір мәтінімен)."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(WELCOME_TEXT, reply_markup=full_base_kb())
        except TelegramBadRequest:
            pass


# --- 7 сынып тақырыптары ---
# Барлық 8 тақырып URL-батырма (Google Drive/Docs), басқанда сілтеме тікелей ашылады,
# сондықтан оларға callback-хэндлер қажет емес. Сілтемелер keyboards.py ішінде (GEO_7_*_URL).


@router.callback_query(F.data == CB_GEO_8)
async def geo_8_handler(callback: CallbackQuery) -> None:
    """"8 сынып география": сол хабарлама тақырыптар тізіміне ауысады."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(GEO_8_TEXT, reply_markup=geo_8_kb())
        except TelegramBadRequest:
            pass


# --- 8 сынып тақырыптары (бос хэндлерлер) ---


# --- 8 сынып тақырыптары ---
# Барлық 9 тақырып URL-батырма (Google Docs), басқанда сілтеме тікелей ашылады,
# сондықтан оларға callback-хэндлер қажет емес. Сілтемелер keyboards.py ішінде (GEO_8_*_URL).


@router.callback_query(F.data == CB_GEO_9)
async def geo_9_handler(callback: CallbackQuery) -> None:
    """"9 сынып география": сол хабарлама тақырыптар тізіміне ауысады."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(GEO_9_TEXT, reply_markup=geo_9_kb())
        except TelegramBadRequest:
            pass


# --- 9 сынып тақырыптары (бос хэндлерлер) ---


# --- 9 сынып тақырыптары ---
# Барлық 10 тақырып URL-батырма (Google Docs/Drive), басқанда сілтеме тікелей ашылады,
# сондықтан оларға callback-хэндлер қажет емес. Сілтемелер keyboards.py ішінде (GEO_9_*_URL).


CHECKING_FRAMES = (
    "⏳ <b>Тексерілуде.</b>",
    "⏳ <b>Тексерілуде..</b>",
    "⌛ <b>Тексерілуде...</b>",
    "🔐 <b>Қолжетімділік тексерілуде...</b>",
)
PRO_LOCKED_TEXT = "🔒⭐ <b>Бұл материалдар PRO деңгейде қолжетімді!</b> 🚀"
CHECK_DELAY = 0.6  # кадрлар арасындағы кідіріс (сек)

# Анимация жүріп жатқанда қайта басылса, қайталамау үшін (пайдаланушы ID)
_checking_users: set[int] = set()


async def show_pro_locked(callback: CallbackQuery) -> None:
    """Тексеру анимациясы + PRO жабық экраны («PRO деңгейге өту» батырмасымен)."""
    await callback.answer()
    if not isinstance(callback.message, Message):
        return

    user_id = callback.from_user.id
    if user_id in _checking_users:
        return  # анимация әлі жүріп жатыр
    _checking_users.add(user_id)

    try:
        status = await callback.message.answer(CHECKING_FRAMES[0])
        for frame in CHECKING_FRAMES[1:]:
            await asyncio.sleep(CHECK_DELAY)
            await safe_edit(status, frame)
        await asyncio.sleep(CHECK_DELAY)
        await status.edit_text(PRO_LOCKED_TEXT, reply_markup=pro_upgrade_kb())
    except TelegramBadRequest:
        pass
    finally:
        _checking_users.discard(user_id)


@router.callback_query(F.data == CB_GRADE_10_11)
async def grade_10_11_handler(callback: CallbackQuery) -> None:
    await show_pro_locked(callback)


@router.callback_query(F.data == CB_QUIZZES)
async def quizzes_handler(callback: CallbackQuery) -> None:
    await show_pro_locked(callback)


@router.callback_query(F.data == CB_PLACEMENT_TEST)
async def placement_test_handler(callback: CallbackQuery) -> None:
    await show_menu(callback, placement_test_kb())  # 1–4 нұсқа


# Placement Test нұсқалары (1–4) — URL-батырмалар (QuizBot), хэндлер қажет емес.
# Сілтемелер: keyboards.py → PLACE_1_URL … PLACE_4_URL


# "Контексттер" — URL-батырма (Google Drive), хэндлер қажет емес.
# Сілтеме: keyboards.py → CONTEXTS_URL


# "GeoAI ассистент" — URL-батырма (@geoaiassistantbot), хэндлер қажет емес.
# Сілтеме: keyboards.py → GEOAI_URL



# --- PRO деңгей ---

# Төлем деректері (қажет болса, осында өзгертіңіз)
CARD_NUMBER = "4400 4300 4571 4687"
KASPI_PHONE = "+77058951332"
OWNER_NAME = "Ақжол Әйлеш"
PRO_PRICE = "4990 тг"

# Жабық PRO каналдың шақыру сілтемесі. Нақты сілтемемен ауыстырыңыз,
# мысалы: "https://t.me/+AbCdEfGh123".
PRO_CHANNEL_LINK = "https://t.me/+mMTenbJ1i9s2MjVi"

# Жабық PRO каналдың ID-і. Бот каналдың админі болса ("Invite users via link"
# құқығымен), әр оқушыға бір рет қолданылатын жеке сілтеме жасалады.
# Әйтпесе жоғарыдағы жалпы PRO_CHANNEL_LINK жіберіледі.
PRO_CHANNEL_ID = -1003929204786
INVITE_LIFETIME = timedelta(days=3)  # жеке сілтеменің жарамдылық мерзімі

PRO_LOADING_FRAMES = (
    "💳 <b>PRO деректері дайындалуда</b>\n\n▰▱▱▱▱▱▱▱",
    "💳 <b>PRO деректері дайындалуда.</b>\n\n▰▰▰▱▱▱▱▱",
    "💳 <b>PRO деректері дайындалуда..</b>\n\n▰▰▰▰▰▱▱▱",
    "✨ <b>PRO деректері дайындалуда...</b>\n\n▰▰▰▰▰▰▰▰",
)
PRO_LOADING_DELAY = 0.45

PRO_TEXT = (
    f"⭐ <b>PRO деңгей — {PRO_PRICE}</b>\n\n"
    "<b>Реквизиттер (Kaspi):</b>\n"
    f"💳 Карта: <code>{CARD_NUMBER}</code>\n"
    f"👤 Алушы: {OWNER_NAME}\n"
    f"📱 Телефон: <code>{KASPI_PHONE}</code>\n\n"
    "Kaspi.kz → Переводы → Клиенту Kaspi → По номеру телефона\n\n"
    "1) «Kaspi-де төлеу» батырмасы Kaspi сайтына апарады.\n"
    "2) Төлемді нөмір арқылы жасап болған соң, «Төледім» батырмасын басып чекті жіберіңіз."
)

PRO_INFO_TEXT = (
    "🌟 <b>PRO ДЕҢГЕЙ МҮМКІНДІКТЕРІ:</b>\n\n"
    "1️⃣ Боттағы тегін материалдардың барлығы\n"
    "2️⃣ <b>1500+</b> Нағыз ҰБТ-да кездесетін сұрақтар викторинасы\n"
    "3️⃣ 7-11 сынып толық <b>Quizzes</b>\n"
    "4️⃣ Авторлық интерактивті карта жаттау сайты (жақында іске қосылады)\n"
    "5️⃣ Авторлық математикалық сауаттылық дайындық сайты (жақында іске қосылады)\n"
    "6️⃣ 🤖 <b>GeoAI assistant-ке шексіз доступ</b>\n"
    "7️⃣ <b>Study buddy</b> табу &amp; Апталық рейтинг\n"
    "8️⃣ Ашық <b>VIP community</b>\n"
    "9️⃣ Қаңтар ҰБТ кезінде күнделікті сливтер"
)

RECEIPT_REQUEST_TEXT = (
    "🧾 Төлем жасаған соң, чектің <b>фотосын</b> немесе <b>PDF файлын</b> осы чатқа жіберіңіз."
)
RECEIPT_CHECKING_TEXT = "⏳ Төлем түбіртегі тексерілуде..."
RECEIPT_PENDING_TEXT = "📨 Чегіңіз админге жіберілді. Растала салысымен сілтеме осы чатқа келеді."
RECEIPT_ALREADY_PENDING_TEXT = "⏳ Сіздің чегіңіз әлі тексерілуде. Күте тұрыңыз."
PAYMENT_REJECTED_TEXT = (
    "❌ <b>Төлем расталмады.</b>\n"
    "Төлем жасалғанын тексеріп, чекті қайта жіберіңіз."
)
SERVICE_UNAVAILABLE_TEXT = "⚠️ Қызмет уақытша қолжетімсіз. Кейінірек қайталап көріңіз."

def payment_success_text() -> str:
    """Төлем расталғаннан кейінгі хабарлама. Сілтеме мәтінде жоқ, тек батырмада."""
    return (
        "🎉 <b>Төлем сәтті тексерілді!</b>\n"
        "Сізге PRO деңгейге толық рұқсат ашылды. "
        "Төмендегі батырма арқылы жабық каналға қосылыңыз.\n\n"
        "<i>⚠️ Ескерту: Кіру жеке сізге арналған, бір рет қана жұмыс істейді "
        "және қауіпсіздік мақсатында қорғалған (көшірілмейді).</i>"
    )


async def make_invite_link(bot: Bot, user_id: int) -> str:
    """Бір рет қолданылатын жеке сілтеме. Жалпы канал сілтемесі ешқашан жіберілмейді."""
    invite = await bot.create_chat_invite_link(
        chat_id=PRO_CHANNEL_ID,
        name=f"PRO {user_id}"[:32],
        member_limit=1,
        expire_date=INVITE_LIFETIME,
        creates_join_request=False,
    )
    return invite.invite_link

_pro_loading_users: set[int] = set()


@router.callback_query(F.data == CB_PRO_LEVEL)
async def pro_level_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    if not isinstance(callback.message, Message):
        return

    user_id = callback.from_user.id
    if user_id in _pro_loading_users:
        return  # анимация әлі жүріп жатыр
    _pro_loading_users.add(user_id)

    try:
        # 1) Жүктелу анимациясы: сол хабарламаның өзі өңделеді (ескі батырмалар жойылады)
        for frame in PRO_LOADING_FRAMES:
            await safe_edit(callback.message, frame)
            await asyncio.sleep(PRO_LOADING_DELAY)

        # 2-3) Әдемі мәтін + төлем батырмалары
        await callback.message.edit_text(
            PRO_TEXT,
            reply_markup=pro_payment_kb(),
        )
    except TelegramBadRequest:
        pass
    finally:
        _pro_loading_users.discard(user_id)


@router.callback_query(F.data == CB_PRO_INFO)
async def pro_info_handler(callback: CallbackQuery) -> None:
    """"ℹ️ PRO деңгейде не бар?": сол хабарламада мүмкіндіктер тізімін көрсетеді."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(PRO_INFO_TEXT, reply_markup=pro_info_kb())
        except TelegramBadRequest:
            pass


@router.callback_query(F.data == CB_PRO_BACK_TO_PAY)
async def pro_back_to_pay_handler(callback: CallbackQuery) -> None:
    """"⬅️ Төлемге қайту": төлем экранын анимациясыз қайтарады."""
    await callback.answer()
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(PRO_TEXT, reply_markup=pro_payment_kb())
        except TelegramBadRequest:
            pass


# --- Чек және админ растауы ---
#
# Ағын: оқушы чек жібереді -> чек админге батырмалармен келеді ->
# админ "✅ Растау" басқанда ғана оқушыға PRO канал сілтемесі барады.


def get_admin_id() -> int | None:
    """Админнің Telegram ID-і (.env ішіндегі ADMIN_ID). Жоқ болса, None."""
    value = os.getenv("ADMIN_ID", "").strip()
    return int(value) if value.isdigit() else None


# Админ шешімін күтіп тұрған оқушылар (қайталап чек жіберуден қорғаныс)
_pending_receipts: set[int] = set()


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    """Өз Telegram ID-іңізді білу үшін (ADMIN_ID-ге жазу керек)."""
    await message.answer(f"🆔 Сіздің Telegram ID: <code>{message.from_user.id}</code>")


@router.callback_query(F.data == CB_I_PAID)
async def i_paid_handler(callback: CallbackQuery) -> None:
    """"✅ Төледім": чек жіберуді сұрайды."""
    await callback.answer()
    if isinstance(callback.message, Message):
        if callback.from_user.id in _pending_receipts:
            await callback.message.answer(RECEIPT_ALREADY_PENDING_TEXT)
        else:
            await callback.message.answer(RECEIPT_REQUEST_TEXT)


@router.message(F.photo | F.document)
async def receipt_handler(message: Message) -> None:
    """Чек (фото немесе файл) келгенде: админге растауға жібереді."""
    user = message.from_user
    admin_id = get_admin_id()
    if admin_id is None:
        logging.error("ADMIN_ID .env ішінде жоқ: чек өңделмеді (пайдаланушы %s)", user.id)
        await message.answer(SERVICE_UNAVAILABLE_TEXT)
        return

    if user.id in _pending_receipts:
        await message.answer(RECEIPT_ALREADY_PENDING_TEXT)
        return
    _pending_receipts.add(user.id)

    await message.answer(RECEIPT_CHECKING_TEXT)

    username = f" (@{html.escape(user.username)})" if user.username else ""
    caption = (
        "🧾 <b>Жаңа чек</b>\n"
        f'👤 <a href="tg://user?id={user.id}">{html.escape(user.full_name)}</a>{username}\n'
        f"🆔 <code>{user.id}</code>\n"
        f"💰 {PRO_PRICE}"
    )
    try:
        await message.copy_to(admin_id, caption=caption, reply_markup=admin_review_kb(user.id))
    except (TelegramBadRequest, TelegramForbiddenError):
        # Мысалы, админ ботқа ешқашан /start жазбаған
        _pending_receipts.discard(user.id)
        logging.exception("Чекті админге (%s) жіберу мүмкін болмады", admin_id)
        await message.answer(SERVICE_UNAVAILABLE_TEXT)
        return

    await message.answer(RECEIPT_PENDING_TEXT)


@router.callback_query(F.data.startswith((CB_PAY_OK + ":", CB_PAY_NO + ":")))
async def review_handler(callback: CallbackQuery) -> None:
    """Админнің "✅ Растау" / "❌ Қабылдамау" шешімі."""
    admin_id = get_admin_id()
    if admin_id is None or callback.from_user.id != admin_id:
        await callback.answer("Рұқсат жоқ", show_alert=True)
        return

    action, _, raw_id = (callback.data or "").partition(":")
    if not raw_id.isdigit() or not isinstance(callback.message, Message):
        await callback.answer()
        return
    user_id = int(raw_id)
    approved = action == CB_PAY_OK

    # Батырмаларды бірінші болып алып тастаймыз: қайталап басылса, екінші рет өңделмейді
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        await callback.answer("Бұл чек бұрын өңделген", show_alert=True)
        return

    _pending_receipts.discard(user_id)

    note = ""
    try:
        if approved:
            try:
                from subscription import activate_subscription

                activate_subscription(user_id)
            except Exception:
                logging.exception("Жазылым мерзімін жазу мүмкін болмады (user=%s)", user_id)
            try:
                link = await make_invite_link(callback.bot, user_id)
            except (TelegramBadRequest, TelegramForbiddenError):
                logging.exception("Жеке сілтеме жасалмады (бот каналдың админі ме?)")
                note = (
                    "\n⚠️ Жеке сілтеме жасалмады. Жалпы сілтеме жіберілген жоқ. "
                    "Бот каналдың админі екенін тексеріңіз."
                )
            else:
                await callback.bot.send_message(
                    user_id,
                    payment_success_text(),
                    reply_markup=pro_invite_kb(link),
                    protect_content=True,
                )
        else:
            await callback.bot.send_message(user_id, PAYMENT_REJECTED_TEXT)
    except TelegramForbiddenError:
        note += "\n⚠️ Оқушы ботты бұғаттаған, хабарлама жетпеді."

    result = "✅ <b>Расталды</b>" if approved else "❌ <b>Қабылданбады</b>"
    try:
        await callback.message.edit_caption(
            caption=f"{callback.message.html_text}\n\n{result}{note}"
        )
    except TelegramBadRequest:
        pass
    await callback.answer("Расталды" if approved else "Қабылданбады")


@router.chat_member()
async def guard_pro_channel(event: ChatMemberUpdated) -> None:
    """Төлемеген немесе мерзімі біткен адамды PRO каналдан шығарады."""
    if event.chat.id != PRO_CHANNEL_ID:
        return
    new = event.new_chat_member
    if new.user.is_bot:
        return
    if new.status not in {"member", "restricted"}:
        return
    if event.old_chat_member.status in {"member", "administrator", "creator", "restricted"}:
        return

    from subscription import is_subscription_active
    from subscription_jobs import kick_from_pro_channel

    if is_subscription_active(new.user.id):
        return
    await kick_from_pro_channel(event.bot, new.user.id, PRO_CHANNEL_ID)
    logging.info("Төлемеген қолданушы каналдан шығарылды: user=%s", new.user.id)
