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
                "If you’re able to help by providing a resource, access, or connection, contact the resident directly. Once the request is fulfilled, you’ll receive 1 point.\n\n"
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
            "Here you can share a resource you have available right now — a skill, service, access, or any other support you’re ready to offer at this moment.\n"
            "Describe your resource according to the short form below and send it to the chat. Your resource will appear in the list of active offers, and once it’s used, you’ll receive a point.\n\n"
            "First, select a **Category**:"
        )
    else:
        text = (
            "Here you can post a request for a resource, support, skill, or access you’re currently looking for.\n"
            "Describe what you need, where, and how soon. Your request will appear in the list of active requests so other members can respond or help.\n\n"
            "First, select a **Category**:"
        )

    # Use unique prefix to avoid conflict with Resources section
    await callback.message.edit_text(
        text,
        reply_markup=get_resource_categories_keyboard(prefix="lot_cat")
    )
    await state.set_state(AddLot.category)
    await callback.answer()


@router.callback_query(AddLot.category, F.data.startswith("lot_cat:"))
async def process_lot_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":", 1)[1]
    await state.update_data(category=category)

    data = await state.get_data()
    lot_type = data.get("lot_type")

    type_label = "Type of Resource"
    type_ex = "(e.g. consultation, introduction, equipment, access, skill, space)"

    # We switch to text input, so we must delete inline keyboard and send new message
    await callback.message.delete()
    await callback.message.answer(
        f"Selected: {category}\n\n"
        f"**{type_label}**\n"
        f"{type_ex}\n\n"
        f"Please type the resource type:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddLot.type_text)
    await callback.answer()


@router.message(AddLot.type_text, F.text)
async def process_lot_type_text(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        # Back to category
        await message.answer("Select a Category:", reply_markup=get_resource_categories_keyboard(prefix="lot_cat"))
        await state.set_state(AddLot.category)
        return

    await state.update_data(type_text=message.text)

    data = await state.get_data()
    lot_type = data.get("lot_type")

    desc_prompt = "Description\n(briefly describe what exactly you’re offering and in what form)" if lot_type == "share" else "Description\n(briefly describe what you’re looking for and in what form)"

    await message.answer(
        f"**{desc_prompt}**",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddLot.description)


@router.message(AddLot.description, F.text)
async def process_lot_description(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await message.answer("Type of Resource:", reply_markup=get_cancel_keyboard())
        await state.set_state(AddLot.type_text)
        return

    await state.update_data(description=message.text)

    # Remove previous Reply keyboard before showing Inline city selection
    await message.answer("Select Location:", reply_markup=ReplyKeyboardRemove())

    # Send city selection keyboard with prefix "lot_city"
    await message.answer(
        "**Location**\n(Select city)",
        reply_markup=get_cities_keyboard(prefix="lot_city")
    )
    await state.set_state(AddLot.location)


@router.callback_query(AddLot.location, F.data.startswith("lot_city:"))
async def process_lot_city(callback: CallbackQuery, state: FSMContext):
    """Handle city selection for Lot"""
    city = callback.data.split(":", 1)[1]
    await state.update_data(location=city)

    data = await state.get_data()
    lot_type = data.get("lot_type")

    avail_prompt = "Availability\n(specific dates, this week, next 14 days, flexible)" if lot_type == "share" else "When Needed\n(ASAP, specific dates, this week, next 14 days, flexible)"

    # Switch back to text input (Availability)
    await callback.message.delete()
    await callback.message.answer(
        f"Selected Location: {city}\n\n"
        f"**{avail_prompt}**",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddLot.availability)
    await callback.answer()


# Handle "Back" from City Selection
@router.callback_query(AddLot.location, F.data == "back_to_lot_description")
async def back_to_lot_description(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Description\n(briefly describe what exactly you’re offering and in what form)",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddLot.description)
    await callback.answer()


@router.message(AddLot.availability, F.text)
async def process_lot_availability(message: Message, state: FSMContext, db: Database):
    if message.text == "🔙 Back":
        # Back to Location selection
        await message.answer("Select Location:", reply_markup=ReplyKeyboardRemove())
        await message.answer(
            "**Location**\n(Select city)",
            reply_markup=get_cities_keyboard(prefix="lot_city")
        )
        await state.set_state(AddLot.location)
        return

    data = await state.get_data()
    availability = message.text

    # Save lot
    lot_id = await db.add_lot(
        user_id=message.from_user.id,
        lot_type=data['lot_type'],
        title=data['type_text'], # Using Type as Title
        description=data['description'],
        category=data['category'],
        location_text=data['location'], # Storing city name here
        availability=availability,
        status="pending"
    )

    await state.clear()

    if lot_id:
        type_emoji = "🎁" if data['lot_type'] == "share" else "🔍"

        await message.answer(
            f"✅ Lot submitted for moderation!\n\n"
            f"{type_emoji} **{data['type_text']}**\n"
            f"🏷 {data['category']}\n"
            f"⏳ An admin will review your lot soon.",
            reply_markup=get_menu_keyboard(message.from_user.id)
        )

        # Notify admins
        # FIX: Removed 'from bot.main import bot' to avoid circular import.
        # Use message.bot instead.
        user = await db.get_user(message.from_user.id)
        for admin_id in ADMIN_IDS:
            try:
                await message.bot.send_message(
                    admin_id,
                    f"🆕 New lot pending moderation!\n\n"
                    f"👤 From: {user['name']} (@{message.from_user.username or 'no username'})\n"
                    f"📋 Type: {type_emoji} {data['lot_type']}\n"
                    f"🏷 Category: {data['category']}\n"
                    f"📌 Title: {data['type_text']}\n"
                    f"📝 Description: {data['description']}\n"
                    f"📍 Location: {data['location']}\n"
                    f"📅 Availability: {availability}",
                    reply_markup=get_lot_moderation_keyboard(lot_id)
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")

        # Show lots menu
        await message.answer(
            "🎯 Lots\n\n"
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
