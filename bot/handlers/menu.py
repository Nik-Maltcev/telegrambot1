from aiogram import Router, F
from aiogram.types import Message
from bot.database import Database
from bot.keyboards import get_menu_keyboard
from bot.config import ADMIN_IDS, CHANNEL_USERNAME

router = Router()


@router.message(F.text == "👤 My Profile")
async def show_profile(message: Message, db: Database):
    """Show user profile"""
    user = await db.get_user(message.from_user.id)
    keyboard = get_menu_keyboard(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.", reply_markup=keyboard)
        return

    profile_text = (
        f"👤 Your Profile\n\n"
        f"Name: {user['name']}\n"
        f"Main City: {user['main_city']}\n"
        f"Current City: {user['current_city']}\n"
        f"About: {user['about']}\n"
        f"Instagram: {user['instagram'] if user['instagram'] else 'Not provided'}\n"
        f"💰 Points: {user['points']}\n"
        f"📅 Registered: {user['registered_at'][:10]}"
    )

    await message.answer(profile_text, reply_markup=keyboard)


@router.message(F.text == "📢 Channel")
async def show_channel(message: Message):
    """Show channel link"""
    keyboard = get_menu_keyboard(message.from_user.id)
    if CHANNEL_USERNAME:
        await message.answer(
            f"📢 Community Channel\n\n"
            f"Join our channel to stay updated:\n"
            f"{CHANNEL_USERNAME}\n\n"
            f"📌 Channel content:\n"
            f"• News and updates\n"
            f"• Resident portraits\n"
            f"• Exchange digest\n"
            f"• New resources digest\n\n"
            f"📍 Pinned: How to earn points?",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "📢 Community Channel\n\n"
            "Channel link will be provided soon.\n"
            "Stay tuned!",
            reply_markup=keyboard
        )
