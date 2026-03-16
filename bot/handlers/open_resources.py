from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.database import Database
from bot.keyboards import get_back_keyboard
from bot.form_data import CITIES
import hashlib
import json

router = Router()

# Карты городов от Hanna (только для этих городов есть ссылки)
CITY_MAPS = {
    "Bangkok 🇹🇭": "https://maps.app.goo.gl/iFcMHwccPhDS9vnA7?g_st=i",
    "Budapest 🇭🇺": "https://maps.app.goo.gl/NZAnT7YWe4XN57x36?g_st=i",
    "Paris 🇫🇷": "https://maps.app.goo.gl/1XQjT77FsS6CcVmN9?g_st=i",
    "Amsterdam 🇳🇱": "https://maps.app.goo.gl/Y3ezvHuKY2Rzd3rZ8?g_st=i",
    "Berlin 🇩🇪": "https://maps.app.goo.gl/fmuAfTu5mexF478e6?g_st=i",
    "Lisbon 🇵🇹": "https://maps.app.goo.gl/cg42PEZaVwtRmPLa7?g_st=i",
    "Istanbul 🇹🇷": "https://maps.app.goo.gl/xYp1DxVdNg4bav8E7?g_st=i",
}


def get_maps_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with all cities"""
    builder = InlineKeyboardBuilder()
    
    for i in range(0, len(CITIES), 2):
        row_btns = []
        city1 = CITIES[i]
        city_hash1 = hashlib.md5(city1.encode()).hexdigest()[:8]
        row_btns.append(InlineKeyboardButton(text=city1, callback_data=f"map:{city_hash1}"))
        
        if i + 1 < len(CITIES):
            city2 = CITIES[i + 1]
            city_hash2 = hashlib.md5(city2.encode()).hexdigest()[:8]
            row_btns.append(InlineKeyboardButton(text=city2, callback_data=f"map:{city_hash2}"))
        
        builder.row(*row_btns)
    
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu"))
    return builder.as_markup()


def find_city_by_hash(city_hash: str) -> str | None:
    """Find city name by its hash"""
    for city in CITIES:
        if hashlib.md5(city.encode()).hexdigest()[:8] == city_hash:
            return city
    return None


@router.message(F.text == "🌎Maps")
async def show_maps_menu(message: Message, db: Database):
    """Show MAPS section - List of cities"""
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "🌎Maps\n\n"
        "Select a city to see the map:",
        reply_markup=get_maps_keyboard()
    )


@router.callback_query(F.data.startswith("map:"))
async def show_city_map(callback: CallbackQuery, db: Database):
    """Show map for selected city"""
    city_hash = callback.data.split(":", 1)[1]
    city = find_city_by_hash(city_hash)
    
    if not city:
        await callback.answer("City not found", show_alert=True)
        return
    
    # Collect all maps for this city
    builder = InlineKeyboardBuilder()
    has_maps = False
    text_parts = [f"🌎 {city}\n"]

    # 1. Hanna's curated map
    hanna_link = CITY_MAPS.get(city)
    if hanna_link:
        has_maps = True
        text_parts.append("🗺 Hanna · Curated places")
        builder.row(InlineKeyboardButton(text="🗺 Open Hanna's Map", url=hanna_link))

    # 2. User-submitted maps from registration data
    all_reg_data = await db.get_all_registration_data()
    for user_data in all_reg_data:
        try:
            reg_data = json.loads(user_data["answer_data"])
            user_maps = reg_data.get("user_maps", [])
            for m in user_maps:
                if m.get("city") == city:
                    has_maps = True
                    user_name = user_data.get("name", "Unknown")
                    map_link = m.get("link", "")
                    if map_link:
                        text_parts.append(f"🗺 {user_name}")
                        builder.row(InlineKeyboardButton(
                            text=f"🗺 Open {user_name}'s Map",
                            url=map_link
                        ))
        except (json.JSONDecodeError, KeyError):
            continue

    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_maps"))

    if has_maps:
        await callback.message.edit_text(
            "\n".join(text_parts),
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.edit_text(
            f"🌎 {city}\n\n"
            f"No maps for this city yet.\n"
            f"You can share yours during registration (section 10|10).",
            reply_markup=builder.as_markup()
        )
    
    await callback.answer()


@router.callback_query(F.data == "back_to_maps")
async def back_to_maps(callback: CallbackQuery):
    """Go back to maps menu"""
    await callback.message.edit_text(
        "🌎Maps\n\n"
        "Select a city to see the map:",
        reply_markup=get_maps_keyboard()
    )
    await callback.answer()
