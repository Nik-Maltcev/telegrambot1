import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database import Database
from bot.keyboards import (
    get_lots_type_keyboard,
    get_add_lot_keyboard,
    get_cancel_keyboard,
    get_menu_keyboard,
    get_lot_moderation_keyboard,
    get_resource_categories_keyboard,
    get_single_select_keyboard,
    get_cities_keyboard
)
from bot.config import ADMIN_IDS
from datetime import datetime

router = Router()
logger = logging.getLogger(__name__)


class AddLot(StatesGroup):
    selecting_type = State() # A or C
    category = State()
    type_text = State()
    description = State()
    location = State()
    availability = State() # Or "When Needed"


@router.message(F.text == "🩵Lots")
async def show_lots_menu(message: Message, db: Database):
    """Show lots section menu"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "🩵Lots\n\n"
        "Here you can manage what you share and what you're looking for.\n\n"
        "Select an option:",
        reply_markup=get_lots_type_keyboard()
    )


# --- B. Browse active resources (Offers) ---
@router.callback_query(F.data == "lots:browse_b")
async def browse_active_offers(callback: CallbackQuery, db: Database):
    await show_active_lots(callback, db, "share", "Active Resources 🫧")


# --- D. Help a resident (Requests) ---
@router.callback_query(F.data == "lots:help_d")
async def browse_active_requests(callback: CallbackQuery, db: Database):
    await show_active_lots(callback, db, "seek", "Active Requests 👀")


async def show_active_lots(callback: CallbackQuery, db: Database, lot_type: str, title_text: str):
    """Helper to show active lots"""
    try:
        lots = await db.get_active_lots(lot_type)

        instructions = ""
        if lot_type == "share":
            instructions = (
                "Here you’ll find a list of active resources shared by community members.\n"
                "You can use a resource in exchange for your point. To proceed, simply contact the owner directly and coordinate the details.\n\n"
            )
        else:
            instructions = (
                "Here you can browse all active requests shared by our residents.\n"
                "If you’re able to help by providing a resource, access, or connection, contact the resident directly. Once the request is fulfilled, you’ll receive 1 point\n\n"
            )

        if not lots:
            await callback.message.edit_text(
                f"{title_text}\n\n"
                f"{instructions}"
                f"No items found in this section yet.",
                reply_markup=get_lots_type_keyboard()
            )
        else:
            lots_text = f"{title_text}\n\n{instructions}"

            for lot in lots:
                username = f"(@{lot['username']})" if lot['username'] else ""
                category = f"🏷 {lot['category']}\n" if lot['category'] else ""
                location = f"📍 {lot['location_text']}\n" if lot['location_text'] else ""

                # Availability / When Needed
                avail_label = "Availability" if lot_type == "share" else "When Needed"
                availability = f"📅 {avail_label}: {lot['availability']}\n" if lot['availability'] else ""

                lots_text += (
                    f"━━━━━━━━━━━━━━━\n"
                    f"📌 {lot['title']}\n"
                    f"{category}"
                    f"📝 {lot['description']}\n"
                    f"{location}"
                    f"{availability}"
                    f"👤 {lot['name']} {username}\n\n"
                )

            if len(lots_text) > 4096:
                await callback.message.delete()
                chunks = [lots_text[i:i+4096] for i in range(0, len(lots_text), 4096)]
                for chunk in chunks:
                    await callback.message.answer(chunk)

                await callback.message.answer(
                    "Select an option:",
                    reply_markup=get_lots_type_keyboard()
                )
            else:
                await callback.message.edit_text(
                    lots_text,
                    reply_markup=get_lots_type_keyboard()
                )

    except Exception as e:
        logger.error(f"Error in show_active_lots: {e}", exc_info=True)
        await callback.answer("An error occurred.", show_alert=True)
    finally:
        try:
            await callback.answer()
        except:
            pass


# --- A. Offer a resource (Share) ---
@router.callback_query(F.data == "lots:offer_a")
async def start_offer_resource(callback: CallbackQuery, state: FSMContext):
    await start_add_lot_flow(callback, state, "share")


# --- C. Post a request (Seek) ---
@router.callback_query(F.data == "lots:post_c")
async def start_post_request(callback: CallbackQuery, state: FSMContext):
    await start_add_lot_flow(callback, state, "seek")


async def start_add_lot_flow(callback: CallbackQuery, state: FSMContext, lot_type: str):
    """Start the add lot flow"""
    await state.update_data(lot_type=lot_type)

    if lot_type == "share":
        text = (
            "Here you can describe a resource you want to share RIGHT NOW to receive 1 point in exchange — a skill, service, access, or any other support you’re ready to offer\n\n"
            "Describe your resource according to the short form below (IT'S IMPORTANT) and send it to the chat. Your resource will appear in the list of active offers, and once it’s used, you’ll receive a point.\n\n"
            "Copy this text and fill in the information following the example in brackets 👇🏻\n\n"
            "Type of Resource:\n"
            "(e.g. consultation, introduction, equipment, access, skill, space)\n"
            "Description:\n"
            "(briefly describe what exactly you’re offering and in what form)\n"
            "Location:\n"
            "(city or online)\n"
            "Availability:\n"
            "(specific dates, this week, next 14 days, flexible)\n\n"
            "EXAMPLE:\n"
            "Type of Resource: english lessons\n"
            "Description: 60 minutes 4 times per month\n"
            "Location: Online\n"
            "Availability: Only this month"
        )
    else:
        text = (
            "Here you can describe a resource, support, skill, or access you’re currently looking for.\n\n"
            "Describe your request according to the short form below (IT'S IMPORTANT) and send it to the chat. Your request will appear in the list of active requests so other members can respond or help.\n\n"
            "Copy this text and fill in the information following the example in brackets 👇🏻\n\n"
            "Type of Resource:\n"
            "(e.g. consultation, introduction, equipment, access, skill, space)\n"
            "Description:\n"
            "(briefly describe what you’re looking for and in what form)\n"
            "Location:\n"
            "(city or online)\n"
            "When Needed:\n"
            "(ASAP, specific dates, this week, next 14 days, flexible)\n\n"
            "EXAMPLE:\n"
            "Type of Resource: english lessons\n"
            "Description: 60 minutes 4 times per month\n"
            "Location: Online\n"
            "When Needed: Only this month"
        )

    # Use unique prefix to avoid conflict with Resources section
    await callback.message.edit_text(
        text,
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddLot.description)
    await callback.answer()





@router.message(AddLot.description, F.text)
async def process_lot_description(message: Message, state: FSMContext, db: Database):
    if message.text.strip() == "\U0001f519 Back":
        # Go back to lots menu
        await message.answer(
            "\U0001f499Lots\n\n"
            "Here you can manage what you share and what you\u2019re looking for.\n\n"
            "Select an option:",
            reply_markup=get_lots_type_keyboard()
        )
        await state.clear()
        return

    # Parse the template text
    text = message.text.strip()
    data = await state.get_data()
    lot_type = data.get("lot_type", "share")

    # Try to extract fields from the template
    import re as _re
    type_match = _re.search(r"Type of Resource[:\s]*([^\n]+)", text, _re.IGNORECASE)
    desc_match = _re.search(r"Description[:\s]*([^\n]+)", text, _re.IGNORECASE)
    loc_match = _re.search(r"Location[:\s]*([^\n]+)", text, _re.IGNORECASE)
    avail_key = "Availability" if lot_type == "share" else "When Needed"
    avail_match = _re.search(rf"{avail_key}[:\s]*([^\n]+)", text, _re.IGNORECASE)

    title = type_match.group(1).strip() if type_match else text[:100].split('\n')[0]
    description = desc_match.group(1).strip() if desc_match else text
    location = loc_match.group(1).strip() if loc_match else ""
    availability = avail_match.group(1).strip() if avail_match else ""

    # Save lot - now auto-approved without moderation
    lot_id = await db.add_lot(
        user_id=message.from_user.id,
        lot_type=lot_type,
        title=title,
        description=description,
        category="", # We removed category selection
        location_text=location,
        availability=availability,
        status="approved"
    )

    await state.clear()

    if lot_id:
        type_emoji = "🎁" if lot_type == "share" else "🔍"
        await message.answer(
            f"✅ Your lot has been published!\n\n"
            f"{type_emoji} **{title}**\n"
            f"It's now visible to other community members.",
            reply_markup=get_menu_keyboard(message.from_user.id)
        )
        await message.answer(
            "🩵Lots\n\n"
            "Here you can manage what you share and what you're looking for.\n\n"
            "Select an option:",
            reply_markup=get_lots_type_keyboard()
        )
    else:
        await message.answer(
            "❌ Failed to add lot. Please try again.",
            reply_markup=get_menu_keyboard(message.from_user.id)
        )


@router.callback_query(F.data == "lots_menu")
async def back_to_lots_menu(callback: CallbackQuery):
    """Go back to lots menu"""
    await callback.message.edit_text(
        "🩵Lots\n\n"
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
