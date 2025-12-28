from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import get_cities_keyboard, get_back_keyboard, get_cities_select_keyboard

router = Router()

@router.message(F.text == "🌎Maps")
async def show_maps_menu(message: Message, db: Database):
    """Show MAPS section - List of cities"""
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    # Use map_city prefix to distinguish from Friends section (which uses city:)
    await message.answer(
        "🌎Maps\n\n"
        "Select a city to see the map resources:",
        reply_markup=get_cities_select_keyboard("map_city", None, set(), "back_to_menu")
    )


@router.callback_query(F.data.startswith("map_city:"))
async def show_city_map(callback: CallbackQuery):
    """Show map for selected city"""
    import hashlib
    from bot.form_data import CITIES

    # helper to find city by hash
    def find_city(h):
        for c in CITIES:
            if hashlib.md5(c.encode()).hexdigest()[:8] == h:
                return c
        return None

    city_hash = callback.data.split(":", 1)[1]
    city = find_city(city_hash)

    if not city:
        await callback.answer("City not found", show_alert=True)
        return

    # Placeholder link logic
    await callback.message.edit_text(
        f"🌎Maps: {city}\n\n"
        f"The map resource for {city} is coming soon!\n"
        f"Stay tuned.",
        reply_markup=get_back_keyboard("back_to_maps")
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_maps")
async def back_to_maps(callback: CallbackQuery):
    """Go back to maps menu"""
    await callback.message.edit_text(
        "🌎Maps\n\n"
        "Select a city to see the map resources:",
        reply_markup=get_cities_select_keyboard("map_city", None, set(), "back_to_menu")
    )
    await callback.answer()
