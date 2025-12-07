import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database import Database
from bot.keyboards import get_lots_type_keyboard, get_add_lot_keyboard

router = Router()
logger = logging.getLogger(__name__)


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
    try:
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
                # Handle potentially missing fields gracefully
                title = lot.get('title', 'No Title')
                description = lot.get('description', '')
                created_at = lot.get('created_at', '')
                date_str = created_at[:10] if created_at else 'Unknown'

                lots_text += (
                    f"━━━━━━━━━━━━━━━\n"
                    f"📌 {title}\n"
                    f"📝 {description}\n"
                    f"📅 Added: {date_str}\n\n"
                )

            if len(lots_text) > 4096:
                # If text is too long, we need to handle it.
                # Since we can't edit one message into multiple, we delete and send new ones.
                await callback.message.delete()

                chunks = [lots_text[i:i+4096] for i in range(0, len(lots_text), 4096)]
                for chunk in chunks:
                    await callback.message.answer(chunk)

                # Add the control buttons at the end
                await callback.message.answer(
                    "Manage your lots:",
                    reply_markup=get_add_lot_keyboard()
                )
            else:
                await callback.message.edit_text(
                    lots_text,
                    reply_markup=get_add_lot_keyboard()
                )

    except Exception as e:
        logger.error(f"Error in show_user_lots: {e}", exc_info=True)
        # Try to inform the user
        try:
            await callback.answer("An error occurred. Please try again.", show_alert=True)
        except:
            pass
    finally:
        # Ensure we always answer the callback to stop the loading animation
        try:
            await callback.answer()
        except:
            pass


@router.callback_query(F.data == "add_lot")
async def start_add_lot(callback: CallbackQuery, state: FSMContext):
    """Start adding a new lot"""
    await callback.message.answer(
        "➕ Add New Lot\n\n"
        "To add a new lot, please follow this format:\n\n"
        "1.  **Title:** A brief, clear title for your lot.\n"
        "2.  **Description:** A detailed description of what you're offering or seeking.\n"
        "3.  **Photos/Videos (Optional):** Attach any relevant media.\n\n"
        "Example:\n"
        "**Title:** Professional Photoshoot in Paris\n"
        "**Description:** I'm a photographer offering a free 1-hour photoshoot in the heart of Paris. You'll receive 20 edited photos. In return, I'm looking for a place to stay for a weekend.\n\n"
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
