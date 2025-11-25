from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import get_cities_keyboard, get_user_card_keyboard, get_back_keyboard

router = Router()


@router.message(F.text == "👥 Friends")
async def show_friends_menu(message: Message, db: Database):
    """Show friends section - list of cities"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "👥 Friends\n\n"
        "Select a city to see community members:",
        reply_markup=get_cities_keyboard()
    )


@router.callback_query(F.data.startswith("city:"))
async def show_city_users(callback: CallbackQuery, db: Database):
    """Show users in selected city"""
    city = callback.data.split(":", 1)[1]
    users = await db.get_users_by_city(city)

    if not users:
        await callback.answer(f"No users found in {city}", show_alert=True)
        return

    # Show list of users
    users_text = f"👥 Friends in {city}\n\n"

    for user in users:
        instagram_info = f" | 📸 @{user['instagram']}" if user['instagram'] else ""
        users_text += (
            f"👤 {user['name']}\n"
            f"📝 {user['about']}\n"
            f"💰 Points: {user['points']}{instagram_info}\n"
            f"User ID: {user['user_id']}\n\n"
        )

    # Split if message is too long
    if len(users_text) > 4096:
        chunks = [users_text[i:i+4096] for i in range(0, len(users_text), 4096)]
        for chunk in chunks:
            await callback.message.answer(chunk)
    else:
        await callback.message.answer(users_text)

    await callback.answer()


@router.callback_query(F.data == "back_to_friends")
async def back_to_friends(callback: CallbackQuery, db: Database):
    """Go back to friends menu"""
    await callback.message.edit_text(
        "👥 Friends\n\n"
        "Select a city to see community members:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()
