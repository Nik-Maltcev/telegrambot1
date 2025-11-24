from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database import Database
from bot.keyboards import get_lots_type_keyboard, get_add_lot_keyboard

router = Router()


class AddLot(StatesGroup):
    lot_type = State()
    title = State()
    description = State()


@router.message(F.text == "🎯 Lots")
async def show_lots_menu(message: Message, db: Database):
    """Show lots section menu"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "🎯 Lots\n\n"
        "Here you can manage what you share and what you're looking for.\n\n"
        "Select an option:",
        reply_markup=get_lots_type_keyboard()
    )


@router.callback_query(F.data.startswith("lots:"))
async def show_user_lots(callback: CallbackQuery, db: Database):
    """Show user's lots (share or seek)"""
    lot_type = callback.data.split(":", 1)[1]
    lots = await db.get_user_lots(callback.from_user.id, lot_type)

    type_emoji = "🎁" if lot_type == "share" else "🔍"
    type_name = "I Share" if lot_type == "share" else "I Seek"

    if not lots:
        await callback.message.edit_text(
            f"{type_emoji} {type_name}\n\n"
            f"You don't have any items in this section yet.\n"
            f"Add your first one!",
            reply_markup=get_add_lot_keyboard()
        )
    else:
        lots_text = f"{type_emoji} {type_name}\n\n"

        for lot in lots:
            lots_text += (
                f"━━━━━━━━━━━━━━━\n"
                f"📌 {lot['title']}\n"
                f"📝 {lot['description']}\n"
                f"📅 Added: {lot['created_at'][:10]}\n\n"
            )

        await callback.message.edit_text(
            lots_text,
            reply_markup=get_add_lot_keyboard()
        )

    await callback.answer()


@router.callback_query(F.data == "add_lot")
async def start_add_lot(callback: CallbackQuery, state: FSMContext):
    """Start adding a new lot"""
    await callback.message.answer(
        "➕ Add New Lot\n\n"
        "What would you like to add?",
        reply_markup=get_lots_type_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "lots_menu")
async def back_to_lots_menu(callback: CallbackQuery):
    """Go back to lots menu"""
    await callback.message.edit_text(
        "🎯 Lots\n\n"
        "Here you can manage what you share and what you're looking for.\n\n"
        "Select an option:",
        reply_markup=get_lots_type_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    """Handle back to menu callback"""
    await callback.message.delete()
    await callback.answer()
