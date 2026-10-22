from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ---------------------------------------------------------------------------
# callback_data мәндері (handlers.py осыларды қолданады)
# ---------------------------------------------------------------------------

# Басты мәзір
CB_FULL_BASE = "full_base"
CB_NOMENCLATURE = "nomenclature"
CB_GRADE_10_11 = "grade_10_11"
CB_QUIZZES = "quizzes"
CB_PLACEMENT_TEST = "placement_test"
PLACE_1_URL = "https://t.me/QuizBot?start=N79U65Pb"
PLACE_2_URL = "https://t.me/QuizBot?start=nOfzyzk8"
PLACE_3_URL = "https://t.me/QuizBot?start=OPty76j2"
PLACE_4_URL = "https://t.me/QuizBot?start=RIY2ObaG"
CONTEXTS_URL = "https://drive.google.com/file/d/1p2FFfxsqWsKLwSdkLZAh-1HsVOjikgQO/view?usp=drivesdk"
GEOAI_URL = "https://t.me/geoaiassistantbot"
CB_PRO_LEVEL = "pro_level"

# "Толық база" ішкі бөлімдері
CB_GEO_7 = "geo_7"
CB_GEO_8 = "geo_8"
CB_GEO_9 = "geo_9"

# 7 сынып география тақырыптары
GEO_7_METHODS_URL = "https://docs.google.com/document/d/1o6OLJDsMgnZ7qzkptn-y6hYTwy8Ut-aa/edit"
GEO_7_LITHOSPHERE_URL = "https://docs.google.com/document/d/16YHBub4OvYpDfOgChwrasQtw2CdNltkU/edit"
GEO_7_ATMOSPHERE_URL = "https://docs.google.com/document/d/1GxXttBvOo4JUtXuI4uF0VhtnfxGhT9_p/edit"
GEO_7_HYDROSPHERE_URL = "https://docs.google.com/document/d/1oled7M31jyxDbCcf9HrbwhjYtxFmTb7D/edit"
GEO_7_BIOSPHERE_URL = "https://drive.google.com/file/d/1N76iBvbwmd41l0aBJpxSQ1PnIrW4hdeo/view"
GEO_7_SOCIAL_URL = "https://docs.google.com/document/d/1zuYcsWZF5_2aI9lMFl16IwAd9xaJn98q/edit"
GEO_7_ECONOMIC_URL = "https://docs.google.com/document/d/1mTCe40NUl-NMvTIqVBznxLXweW1syhu1/edit"
GEO_7_POLITICAL_URL = "https://docs.google.com/document/d/1xGSVKYAq8pnsqzIdvx74hRZyxluN3H8v/edit"
CB_BACK_TO_GRADES = "back_to_grades"

# 8 сынып география тақырыптары
GEO_8_METHODS_URL = "https://docs.google.com/document/d/1WIw7GW-Jmov1Xdw8dcP69LEb4ZpcoKvM/edit"
GEO_8_CARTOGRAPHY_URL = "https://docs.google.com/document/d/1DxJ7qGswKWDaaE7Bum7l0AmIvCbrd3r2/edit"
GEO_8_LITHOSPHERE_URL = "https://docs.google.com/document/d/1tjGlDbde6H9ZpdSIqPio-OnRCP4RPxSr/edit"
GEO_8_ATMOSPHERE_URL = "https://docs.google.com/document/d/1Pvx8UCZyY2eTKJosq0SXRUG8wht0WgJf/edit"
GEO_8_HYDROSPHERE_URL = "https://docs.google.com/document/d/1gui4ns-mSpuTtPwuEfzAFEkN5YiKAWvO/edit"
GEO_8_BIOSPHERE_URL = "https://docs.google.com/document/d/1IquALRu_KStWw2mhYM5Cxx7oYaBwEdGN/edit"
GEO_8_SOCIAL_URL = "https://docs.google.com/document/d/14NLH6LIo1V4K4GTIlfyUomx33FoyxZoe/edit"
GEO_8_ECONOMIC_URL = "https://docs.google.com/document/d/1fKcj2mqO7lKQfkl-e82hVBCqUnGCy6k_/edit"
GEO_8_POLITICAL_URL = "https://docs.google.com/document/d/17sejhIJVlsUq8Uq5QS-ERBYsh50xbaAp/edit"

# 9 сынып география тақырыптары
GEO_9_METHODS_URL = "https://docs.google.com/document/d/1rYkNI0C7mRx63e7rL14wKQTy3X5qlHRo/edit"
GEO_9_CARTOGRAPHY_URL = "https://docs.google.com/document/d/1uUo7Oli2gbXRac8XjSZqoXEvN8zCg_K_/edit"
GEO_9_BIOSPHERE_URL = "https://docs.google.com/document/d/1wRd8uTq2yTPhJN2irA1OUXR02wEWX0cd/edit"
GEO_9_LITHOSPHERE_URL = "https://docs.google.com/document/d/1DEvVORV7C8dP54ZSIrOytgHxc45FRD7y/edit"
GEO_9_ATMOSPHERE_URL = "https://drive.google.com/file/d/13hF9HYgpysL0HXFXG0ptXkhlXV6N1DlI/view?usp=drivesdk"
GEO_9_HYDROSPHERE_URL = "https://drive.google.com/file/d/1hSoF1ZwjZ7dH2J6KL5fbx7R0m7lMxcGG/view?usp=drivesdk"
GEO_9_SOCIAL_URL = "https://docs.google.com/document/d/15A7PG9meSzvVN7A7bxEJLyUuyFLoa9kw/edit"
GEO_9_ECONOMIC_URL = "https://docs.google.com/document/d/1somx7X7x1ixacNX7Ez8dC1fd6y-YHcSb/edit"
GEO_9_WORLD_ECONOMY_URL = "https://docs.google.com/document/d/1F3qgoN2Qw-YiA216VlurSZuZeDFdMuuD/edit"
GEO_9_POLITICAL_URL = "https://docs.google.com/document/d/1WRpWD1vbZSklAZxB7EzeZGiJ42lHknWs/edit"

# "Номенклатура" ішкі бөлімдері
CB_CONTINENTS = "nom_continents"
CB_OCEANS = "nom_oceans"

# Материктер
EURASIA_URL = "https://drive.google.com/file/d/1jv0TXvwkcXcz5Dppz-6ncBEqnitBQErb/view?usp=drivesdk"
NORTH_AMERICA_URL = "https://drive.google.com/file/d/1cQ7oIybPtnXRDyU7o5k8DNcYjU6cndqh/view?usp=drivesdk"
AFRICA_URL = "https://drive.google.com/file/d/14__3DsM0MtGUK5Ks6ApSZtAzRCfXGipg/view?usp=drivesdk"
SOUTH_AMERICA_URL = "https://drive.google.com/file/d/1rPp8SPlsn9-tdCTZMs74hj9wSQU9kbF1/view?usp=drivesdk"
ANTARCTICA_URL = "https://drive.google.com/file/d/1tufk2hXNZvNFM6QhXsvXBK6SAE2VjSaa/view?usp=drivesdk"
AUSTRALIA_URL = "https://drive.google.com/file/d/1GJJYvEvTFjJxCwY64ob_xdwpbsjrNvbW/view?usp=drivesdk"

# Мұхиттар
PACIFIC_URL = "https://drive.google.com/file/d/1hvkSWR6CjXFUnMLW2pAPdKuOS-MHh3g_/view?usp=drivesdk"
ATLANTIC_URL = "https://drive.google.com/file/d/1En9dy1tHKJTzOZfzy4z1gUp9xLtG-5av/view?usp=drivesdk"
INDIAN_URL = "https://drive.google.com/file/d/1d0HXJO6iKLHJ3b5DMrk4mNYtgNHKmgbF/view?usp=drivesdk"
ARCTIC_URL = "https://drive.google.com/file/d/15ISzO4TPJZgryC8wFqRZNKGlhVg2Q4Ef/view?usp=drivesdk"

# Навигация
CB_BACK_TO_MAIN = "back"
CB_BACK_TO_NOMENCLATURE = "back_to_nomenclature"
BTN_BACK = "⬅️ Артқа"

# ---------------------------------------------------------------------------
# Батырмалар тізімі: (батырма мәтіні, callback_data)
# ---------------------------------------------------------------------------

MAIN_MENU_BUTTONS = (
    ("🌍 Толық база", CB_FULL_BASE),
    ("🗺 Номенклатура", CB_NOMENCLATURE),
    ("🎓 10-11 сынып толық база", CB_GRADE_10_11),
    ("🧩 Quizzes", CB_QUIZZES),
    ("📝 Placement Test", CB_PLACEMENT_TEST),
    ("📚 Контексттер", CONTEXTS_URL),  # Google Drive файлы (URL-батырма)
    ("🤖 GeoAI ассистент", GEOAI_URL),  # @geoaiassistantbot (URL-батырма)
    ("🏆 PRO деңгей", CB_PRO_LEVEL),
)

PLACEMENT_BUTTONS = (
    ("1 нұсқа", PLACE_1_URL),  # QuizBot сілтемесі (URL-батырма)
    ("2 нұсқа", PLACE_2_URL),  # QuizBot сілтемесі (URL-батырма)
    ("3 нұсқа", PLACE_3_URL),  # QuizBot сілтемесі (URL-батырма)
    ("4 нұсқа", PLACE_4_URL),  # QuizBot сілтемесі (URL-батырма)
)

FULL_BASE_BUTTONS = (
    ("7 сынып география", CB_GEO_7),
    ("8 сынып география", CB_GEO_8),
    ("9 сынып география", CB_GEO_9),
)

GEO_7_BUTTONS = (
    ("1. География зерттеу әдістері және ғалымдар", GEO_7_METHODS_URL),  # Google Docs (URL-батырма)
    ("2. Литосфера", GEO_7_LITHOSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("3. Атмосфера", GEO_7_ATMOSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("4. Гидросфера", GEO_7_HYDROSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("5. Биосфера", GEO_7_BIOSPHERE_URL),  # Google Drive файлы (URL-батырма)
    ("6. Әлеуметтік география", GEO_7_SOCIAL_URL),  # Google Docs құжаты (URL-батырма)
    ("7. Экономикалық география", GEO_7_ECONOMIC_URL),  # Google Docs құжаты (URL-батырма)
    ("8. Елтану және саяси география", GEO_7_POLITICAL_URL),  # Google Docs (URL-батырма)
)

GEO_8_BUTTONS = (
    ("1. Географиялық зерттеу әдістері", GEO_8_METHODS_URL),  # Google Docs құжаты (URL-батырма)
    ("2. Картография және геоинформатика", GEO_8_CARTOGRAPHY_URL),  # Google Docs құжаты (URL-батырма)
    ("3. Литосфера", GEO_8_LITHOSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("4. Атмосфера", GEO_8_ATMOSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("5. Гидросфера", GEO_8_HYDROSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("6. Биосфера", GEO_8_BIOSPHERE_URL),  # Google Docs құжаты (URL-батырма)
    ("7. Әлеуметтік география", GEO_8_SOCIAL_URL),  # Google Docs құжаты (URL-батырма)
    ("8. Экономикалық география", GEO_8_ECONOMIC_URL),  # Google Docs құжаты (URL-батырма)
    ("9. Елтану және саяси география", GEO_8_POLITICAL_URL),  # Google Docs құжаты (URL-батырма)
)

GEO_9_BUTTONS = (
    ("1. Географиялық зерттеу әдістері", GEO_9_METHODS_URL),  # Google Docs (URL-батырма)
    ("2. Картография және геоинформатика", GEO_9_CARTOGRAPHY_URL),  # Google Docs (URL-батырма)
    ("3. Биосфера", GEO_9_BIOSPHERE_URL),  # Google Docs (URL-батырма)
    ("4. Литосфера", GEO_9_LITHOSPHERE_URL),  # Google Docs (URL-батырма)
    ("5. Атмосфера", GEO_9_ATMOSPHERE_URL),  # Google Drive файлы (URL-батырма)
    ("6. Гидросфера", GEO_9_HYDROSPHERE_URL),  # Google Drive файлы (URL-батырма)
    ("7. Әлеуметтік география", GEO_9_SOCIAL_URL),  # Google Docs (URL-батырма)
    ("8. Экономикалық география", GEO_9_ECONOMIC_URL),  # Google Docs (URL-батырма)
    ("9. Дүниежүзілік шаруашылық", GEO_9_WORLD_ECONOMY_URL),  # Google Docs (URL-батырма)
    ("10. Елтану", GEO_9_POLITICAL_URL),  # Google Docs (URL-батырма)
)

NOMENCLATURE_BUTTONS = (
    ("Материктер", CB_CONTINENTS),
    ("Мұхиттар", CB_OCEANS),
)

CONTINENT_BUTTONS = (
    ("Еуразия", EURASIA_URL),  # Google Drive файлы (URL-батырма)
    ("Солтүстік Америка", NORTH_AMERICA_URL),  # Google Drive файлы (URL-батырма)
    ("Африка", AFRICA_URL),  # Google Drive файлы (URL-батырма)
    ("Оңтүстік Америка", SOUTH_AMERICA_URL),  # Google Drive файлы (URL-батырма)
    ("Антарктида", ANTARCTICA_URL),  # Google Drive файлы (URL-батырма)
    ("Австралия", AUSTRALIA_URL),  # Google Drive файлы (URL-батырма)
)

OCEAN_BUTTONS = (
    ("Тынық мұхиты", PACIFIC_URL),  # Google Drive файлы (URL-батырма)
    ("Атлант мұхиты", ATLANTIC_URL),  # Google Drive файлы (URL-батырма)
    ("Үнді мұхиты", INDIAN_URL),  # Google Drive файлы (URL-батырма)
    ("Солтүстік Мұзды мұхиты", ARCTIC_URL),  # Google Drive файлы (URL-батырма)
)


# ---------------------------------------------------------------------------
# Пернетақталар
# ---------------------------------------------------------------------------


def _column_kb(
    buttons: tuple[tuple[str, str], ...],
    back_callback: str | None = None,
) -> InlineKeyboardMarkup:
    """Батырмаларды тігінен, бір бағанға тізеді. back_callback болса, соңына "Артқа" қосады.

    Әр батырма: (мәтін, callback_data). Егер екінші мән "https://" деп басталса,
    ол URL-батырма болады (басқанда сілтеме ашылады, хэндлер қажет емес).
    """
    builder = InlineKeyboardBuilder()
    for text, target in buttons:
        if target.startswith(("https://", "http://")):
            builder.button(text=text, url=target)
        else:
            builder.button(text=text, callback_data=target)
    if back_callback:
        builder.button(text=BTN_BACK, callback_data=back_callback)
    builder.adjust(1)  # әр қатарда 1 батырма
    return builder.as_markup()


def pro_upgrade_kb() -> InlineKeyboardMarkup:
    """"PRO деңгейге өту" батырмасы (10-11 сынып бөлімінің жабық хабарламасы үшін)."""
    return _column_kb((("⭐ PRO деңгейге өту", CB_PRO_LEVEL),))


KASPI_PAY_URL = "https://kaspi.kz"  # Kaspi ресми басты беті
CB_I_PAID = "i_paid"
CB_PRO_INFO = "pro_info"
CB_PRO_BACK_TO_PAY = "pro_back_to_pay"


def pro_invite_kb(invite_url: str) -> InlineKeyboardMarkup:
    """Бір реттік каналға кіру батырмасы (сілтеме мәтінде көрсетілмейді)."""
    return _column_kb((("🔗 Каналға кіру", invite_url),))


def pro_payment_kb() -> InlineKeyboardMarkup:
    """PRO төлем экраны: Kaspi (URL), Төледім, PRO ақпараты және Артқа."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔴 Kaspi-де төлеу", url=KASPI_PAY_URL)
    builder.button(text="✅ Төледім", callback_data=CB_I_PAID)
    builder.button(text="🟣 PRO деңгейде не бар?", callback_data=CB_PRO_INFO)
    builder.button(text="⬅️ Артқа", callback_data=CB_BACK_TO_MAIN)
    builder.adjust(1)
    return builder.as_markup()


CB_PAY_OK = "pay_ok"
CB_PAY_NO = "pay_no"


def admin_review_kb(user_id: int) -> InlineKeyboardMarkup:
    """Админге келетін чектің астындағы батырмалар: Растау / Қабылдамау."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Растау", callback_data=f"{CB_PAY_OK}:{user_id}")
    builder.button(text="❌ Қабылдамау", callback_data=f"{CB_PAY_NO}:{user_id}")
    builder.adjust(2)
    return builder.as_markup()


def pro_info_kb() -> InlineKeyboardMarkup:
    """PRO мүмкіндіктері экраны: Төлемге қайту."""
    return _column_kb((("⬅️ Төлемге қайту", CB_PRO_BACK_TO_PAY),))


def main_menu_kb(visible: int | None = None) -> InlineKeyboardMarkup:
    """Басты мәзір (батырмалар тігінен).

    visible — алғашқы неше батырманы көрсету керек (анимациялы ашылу үшін).
    None болса, барлық батырма көрсетіледі.
    """
    return _column_kb(MAIN_MENU_BUTTONS[:visible])


def full_base_kb() -> InlineKeyboardMarkup:
    """"Толық база": 7, 8, 9 сынып + Артқа."""
    return _column_kb(FULL_BASE_BUTTONS, back_callback=CB_BACK_TO_MAIN)


def geo_7_kb() -> InlineKeyboardMarkup:
    """7 сынып география: 8 тақырып + Артқа (сынып таңдауға)."""
    return _column_kb(GEO_7_BUTTONS, back_callback=CB_BACK_TO_GRADES)


def geo_8_kb() -> InlineKeyboardMarkup:
    """8 сынып география: 9 тақырып + Артқа (сынып таңдауға)."""
    return _column_kb(GEO_8_BUTTONS, back_callback=CB_BACK_TO_GRADES)


def geo_9_kb() -> InlineKeyboardMarkup:
    """9 сынып география: 10 тақырып + Артқа (сынып таңдауға)."""
    return _column_kb(GEO_9_BUTTONS, back_callback=CB_BACK_TO_GRADES)


def placement_test_kb() -> InlineKeyboardMarkup:
    """Placement Test: 4 нұсқа + Артқа (басты мәзірге)."""
    return _column_kb(PLACEMENT_BUTTONS, back_callback=CB_BACK_TO_MAIN)


def nomenclature_kb() -> InlineKeyboardMarkup:
    """"Номенклатура": Материктер, Мұхиттар + Артқа (басты мәзірге)."""
    return _column_kb(NOMENCLATURE_BUTTONS, back_callback=CB_BACK_TO_MAIN)


def continents_kb() -> InlineKeyboardMarkup:
    """Материктер тізімі + Артқа (Номенклатураға)."""
    return _column_kb(CONTINENT_BUTTONS, back_callback=CB_BACK_TO_NOMENCLATURE)


def oceans_kb() -> InlineKeyboardMarkup:
    """Мұхиттар тізімі + Артқа (Номенклатураға)."""
    return _column_kb(OCEAN_BUTTONS, back_callback=CB_BACK_TO_NOMENCLATURE)
