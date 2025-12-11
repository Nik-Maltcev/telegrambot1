from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import (
    get_main_menu_keyboard, get_admin_menu_keyboard, get_cancel_keyboard,
    get_skill_categories_keyboard, get_skill_items_keyboard, get_multiselect_keyboard
)
from bot.config import ADMIN_IDS
from bot.form_data import SKILL_CATEGORIES, OFFER_FORMATS, INTERACTION_FORMATS, RESULT_TYPES
import json

router = Router()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, db: Database):
    """Cancel current operation and return to menu"""
    await state.clear()
    user = await db.get_user(message.from_user.id)
    
    if user:
        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()
        await message.answer("✅ Operation cancelled. Back to menu.", reply_markup=keyboard)
    else:
        await message.answer("Operation cancelled. Use /start to register.")


@router.message(Command("myid"))
async def cmd_myid(message: Message):
    """Show user's Telegram ID"""
    await message.answer(
        f"Your Telegram ID: `{message.from_user.id}`\n\n"
        f"Admin IDs configured: {ADMIN_IDS}\n"
        f"You are admin: {message.from_user.id in ADMIN_IDS}",
        parse_mode="Markdown"
    )


class Registration(StatesGroup):
    name = State()
    main_city = State()
    about = State()
    current_city = State()
    instagram = State()

    # Questionnaire states
    skill_category = State()
    skill_items = State()
    offer_formats = State()
    interaction_format = State()
    result_type = State()

    # Final step
    waiting_for_invite_code = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database):
    """Handle /start command"""
    await state.clear()
    user = await db.get_user(message.from_user.id)

    if user:
        # User already registered
        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()

        await message.answer(
            f"👋 Welcome back, {user['name']}!\n\n"
            f"Choose an option from the menu below:",
            reply_markup=keyboard
        )
    else:
        # New user
        # Initialize default lists for multiselects
        await state.update_data(
            selected_skill_items=[],
            selected_offer_formats=[],
            selected_interaction_formats=[],
            selected_result_types=[]
        )

        # Start registration flow - video intro
        video_url = "https://www.youtube.com/watch?v=z1MgFIpSqJk&list=RDz1MgFIpSqJk&start_radio=1"

        # Use simple message with link instead of video to avoid API errors
        await message.answer(
            f"👋 Welcome to JOYSEEKERS!\n\n"
            f"Watch our intro: {video_url}\n\n"
            "This is a closed international community for talented, successful, "
            "and aspiring people who are ready to share their resources and skills "
            "on a voluntary basis.\n\n"
            "Let's get you registered!\n\n"
            "Please enter your name:",
            reply_markup=get_cancel_keyboard()
        )

        await state.set_state(Registration.name)


@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext):
    """Process name input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(name=message.text)
    await message.answer(
        "Great! Now, please enter the city where you are usually located:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.main_city)


@router.message(Registration.main_city, F.text)
async def process_main_city(message: Message, state: FSMContext):
    """Process main city input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(main_city=message.text)
    await message.answer(
        "Tell us a bit about yourself (brief intro):\n\n"
        "For example •Artist and community owner•",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.about)


@router.message(Registration.about, F.text)
async def process_about(message: Message, state: FSMContext):
    """Process about input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(about=message.text)
    await message.answer(
        "What is your current city?",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.current_city)


@router.message(Registration.current_city, F.text)
async def process_current_city(message: Message, state: FSMContext):
    """Process current city input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(current_city=message.text)
    await message.answer(
        "Please enter your Instagram username (or send '-' if you don't have one):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.instagram)


@router.message(Registration.instagram, F.text)
async def process_instagram(message: Message, state: FSMContext):
    """Process Instagram and transition to Questionnaire"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    instagram = message.text if message.text != "-" else ""
    await state.update_data(instagram=instagram)

    # Transition to Questionnaire
    await message.answer(
        "🩵 Now, let's fill out your Professional Profile (Skills & Knowledge).\n"
        "This helps us integrate you into the community resource database.\n\n"
        "Please select your **Category of Expertise**:",
        reply_markup=get_skill_categories_keyboard()
    )
    await state.set_state(Registration.skill_category)


# --- Questionnaire Handlers ---

@router.callback_query(Registration.skill_category, F.data.startswith("q_cat:"))
async def process_skill_category(callback: CallbackQuery, state: FSMContext):
    category_key = callback.data.split(":")[1]
    category_name = SKILL_CATEGORIES[category_key]["name"]

    await state.update_data(current_category=category_key)

    # Prepare for item selection
    # We load previously selected items if any (though logic here implies single pass for now,
    # but let's be robust)
    data = await state.get_data()
    selected_items = set(data.get("selected_skill_items", []))

    await callback.message.edit_text(
        f"Category: {category_name}\n\n"
        "Select specific skills/areas (you can select multiple):",
        reply_markup=get_skill_items_keyboard(category_key, selected_items)
    )
    await state.set_state(Registration.skill_items)
    await callback.answer()


@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))
async def process_skill_item_toggle(callback: CallbackQuery, state: FSMContext):
    import hashlib
    # We need to find which item matches the hash
    item_hash = callback.data.split(":")[1]

    data = await state.get_data()
    category_key = data.get("current_category")
    items_list = SKILL_CATEGORIES.get(category_key, {}).get("items", [])

    # Find item
    target_item = None
    for item in items_list:
        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:
            target_item = item
            break

    if target_item:
        selected_items = set(data.get("selected_skill_items", []))
        if target_item in selected_items:
            selected_items.remove(target_item)
        else:
            selected_items.add(target_item)

        await state.update_data(selected_skill_items=list(selected_items))

        # Update keyboard
        await callback.message.edit_reply_markup(
            reply_markup=get_skill_items_keyboard(category_key, selected_items)
        )

    await callback.answer()

@router.callback_query(Registration.skill_items, F.data == "q_back_cat")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Please select your **Category of Expertise**:",
        reply_markup=get_skill_categories_keyboard()
    )
    await state.set_state(Registration.skill_category)
    await callback.answer()

@router.callback_query(Registration.skill_items, F.data == "q_item_done")
async def finish_skill_items(callback: CallbackQuery, state: FSMContext):
    # Move to Offer Formats
    data = await state.get_data()
    selected = set(data.get("selected_offer_formats", []))

    await callback.message.edit_text(
        "2. Formats You Offer (Select multiple):",
        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done")
    )
    await state.set_state(Registration.offer_formats)
    await callback.answer()


# Formats Handlers
@router.callback_query(Registration.offer_formats, F.data.startswith("q_fmt:"))
async def toggle_offer_format(callback: CallbackQuery, state: FSMContext):
    import hashlib
    item_hash = callback.data.split(":")[1]

    data = await state.get_data()
    selected = set(data.get("selected_offer_formats", []))

    target_item = None
    for item in OFFER_FORMATS:
        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:
            target_item = item
            break

    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)

        await state.update_data(selected_offer_formats=list(selected))
        await callback.message.edit_reply_markup(
            reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done")
        )

    await callback.answer()

@router.callback_query(Registration.offer_formats, F.data == "q_fmt_done")
async def finish_offer_formats(callback: CallbackQuery, state: FSMContext):
    # Move to Interaction Formats
    data = await state.get_data()
    selected = set(data.get("selected_interaction_formats", []))

    await callback.message.edit_text(
        "3. Interaction Format:",
        reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done")
    )
    await state.set_state(Registration.interaction_format)
    await callback.answer()

# Interaction Handlers
@router.callback_query(Registration.interaction_format, F.data.startswith("q_int:"))
async def toggle_interaction_format(callback: CallbackQuery, state: FSMContext):
    import hashlib
    item_hash = callback.data.split(":")[1]

    data = await state.get_data()
    selected = set(data.get("selected_interaction_formats", []))

    target_item = None
    for item in INTERACTION_FORMATS:
        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:
            target_item = item
            break

    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)

        await state.update_data(selected_interaction_formats=list(selected))
        await callback.message.edit_reply_markup(
            reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done")
        )

    await callback.answer()

@router.callback_query(Registration.interaction_format, F.data == "q_int_done")
async def finish_interaction_formats(callback: CallbackQuery, state: FSMContext):
    # Move to Result Types
    data = await state.get_data()
    selected = set(data.get("selected_result_types", []))

    await callback.message.edit_text(
        "4. Type of Result:",
        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done")
    )
    await state.set_state(Registration.result_type)
    await callback.answer()

# Result Types Handlers
@router.callback_query(Registration.result_type, F.data.startswith("q_res:"))
async def toggle_result_type(callback: CallbackQuery, state: FSMContext):
    import hashlib
    item_hash = callback.data.split(":")[1]

    data = await state.get_data()
    selected = set(data.get("selected_result_types", []))

    target_item = None
    for item in RESULT_TYPES:
        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:
            target_item = item
            break

    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)

        await state.update_data(selected_result_types=list(selected))
        await callback.message.edit_reply_markup(
            reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done")
        )

    await callback.answer()

@router.callback_query(Registration.result_type, F.data == "q_res_done")
async def finish_questionnaire(callback: CallbackQuery, state: FSMContext):
    # Questionnaire Done. Now Ask for Invite Code.

    await callback.message.edit_text(
        "✅ Questionnaire completed!\n\n"
        "🔒 This is a private community. To finish registration, please enter your **Invite Token**:\n"
        "(If you are an admin, you can type 'admin' to bypass if configured, or just use a token)"
    )
    # We must reset the reply keyboard or show cancel?
    # The user is in an inline flow. We need to switch back to text input.
    # We can delete the inline message or keep it.

    await state.set_state(Registration.waiting_for_invite_code)
    await callback.answer()


# --- Invite Code Handler ---

@router.message(Registration.waiting_for_invite_code, F.text)
async def process_invite_code(message: Message, state: FSMContext, db: Database):
    token = message.text.strip()

    # Check if admin bypass
    if token.lower() == "admin" and message.from_user.id in ADMIN_IDS:
        is_valid = True
    else:
        is_valid = await db.is_valid_token(token)

    if not is_valid:
        await message.answer("❌ Invalid or expired invite token. Please try again.")
        return

    # Valid token
    data = await state.get_data()

    # Save user
    success = await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=data.get('name', 'Unknown'),
        main_city=data.get('main_city', 'Unknown'),
        current_city=data.get('current_city', 'Unknown'),
        about=data.get('about', ''),
        instagram=data.get('instagram', ''),
        points=0
    )

    if success:
        # Mark token as used
        if token.lower() != "admin":
            await db.use_invite_token(token)

        # Save Questionnaire Data
        user_id = message.from_user.id
        await db.add_user_answer(user_id, "skills", json.dumps(data.get("selected_skill_items", [])))
        await db.add_user_answer(user_id, "offer_formats", json.dumps(data.get("selected_offer_formats", [])))
        await db.add_user_answer(user_id, "interaction_formats", json.dumps(data.get("selected_interaction_formats", [])))
        await db.add_user_answer(user_id, "result_types", json.dumps(data.get("selected_result_types", [])))

        await state.clear()

        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()

        await message.answer(
            f"Registration completed!\n\n"
            f"﹡Name - {data.get('name')}\n"
            f"﹡Main City - {data.get('main_city')}\n"
            f"﹡Current City - {data.get('current_city')}\n"
            f"﹡About - {data.get('about')}\n"
            f"﹡Instagram - @{data.get('instagram') if data.get('instagram') else 'Not provided'}\n"
            f"Points: 0",
            reply_markup=keyboard
        )
    else:
        await message.answer("❌ An error occurred during registration. Please try again with /start")
