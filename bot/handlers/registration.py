from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot.database import Database
from bot.keyboards import (
    get_main_menu_keyboard, get_admin_menu_keyboard, get_cancel_keyboard,
    get_skill_categories_keyboard, get_skill_items_keyboard, get_multiselect_keyboard,
    get_single_select_keyboard, get_skip_keyboard, get_section_intro_keyboard,
    get_cities_select_keyboard, get_category_keyboard, get_category_items_keyboard,
    get_confirmation_keyboard
)
from bot.config import ADMIN_IDS
from bot.form_data import (
    SKILL_CATEGORIES, OFFER_FORMATS, INTERACTION_FORMATS, RESULT_TYPES,
    CITIES, INTRO_CATEGORIES, INTRO_FORMATS,
    PROPERTY_TYPES, PROPERTY_USAGE_FORMAT, PROPERTY_DURATION, PROPERTY_CAPACITY,
    CAR_USAGE_CONDITIONS, CAR_DURATION, CAR_CONDITIONS, CAR_PASSENGERS,
    EQUIPMENT_TYPES, EQUIPMENT_ACCESS_FORMAT, EQUIPMENT_DURATION, EQUIPMENT_RESPONSIBILITY,
    AIRCRAFT_TYPES, AIRCRAFT_USAGE_FORMAT, AIRCRAFT_SAFETY, AIRCRAFT_EXPENSES,
    VESSEL_TYPES, VESSEL_USAGE_FORMAT, VESSEL_SAFETY, VESSEL_FINANCIAL,
    SPECIALIST_CATEGORIES, SPECIALIST_CONNECTION_TYPE,
    ART_FORMS, ART_AUTHOR_TYPE
)
import json
import hashlib

router = Router()


def find_item_by_hash(items_list, item_hash):
    """Helper to find item by its hash"""
    for item in items_list:
        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:
            return item
    return None


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
    instagram = State()

    # Skills section
    skill_category = State()
    skill_items = State()
    offer_formats = State()
    interaction_format = State()
    result_type = State()

    # Personal Introductions section
    intro_section = State()
    intro_category = State()
    intro_items = State()
    intro_location = State()
    intro_format = State()

    # Real Estate section
    real_estate_section = State()
    property_location = State() # Moved first
    property_type = State()
    property_usage = State()
    property_duration = State()
    property_capacity = State()

    # Cars section
    cars_section = State()
    car_location = State() # Moved first
    car_info = State()
    car_usage = State()
    car_duration = State()
    car_conditions = State()
    car_passengers = State()

    # Equipment section
    equipment_section = State()
    equipment_location = State() # Moved first
    equipment_types = State()
    equipment_access = State()
    equipment_duration = State()
    equipment_responsibility = State()

    # Air Transport section
    aircraft_section = State()
    aircraft_location = State() # Moved first
    aircraft_type = State()
    aircraft_usage = State()
    aircraft_safety = State()
    aircraft_expenses = State()

    # Water Transport section
    vessel_section = State()
    vessel_location = State() # Moved first
    vessel_type = State()
    vessel_usage = State()
    vessel_safety = State()
    vessel_financial = State()

    # Specialists section
    specialist_section = State()
    specialist_category = State()
    specialist_items = State()
    specialist_connection = State()
    specialist_name = State()
    specialist_contact = State()
    specialist_referral = State()
    specialist_loop_confirm = State() # New state for loop

    # Artworks section
    artwork_section = State()
    art_form = State()
    art_author = State()
    art_author_name = State()
    art_location = State()
    art_photo = State() # New state

    # Final step
    waiting_for_invite_code = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database):
    """Handle /start command"""
    await state.clear()
    user = await db.get_user(message.from_user.id)

    if user:
        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()
        await message.answer(
            f"👋 Welcome back, {user['name']}!\n\nChoose an option from the menu below:",
            reply_markup=keyboard
        )
    else:
        await state.update_data(
            selected_skill_items=[], selected_offer_formats=[],
            selected_interaction_formats=[], selected_result_types=[],
            selected_intro_items=[], selected_intro_formats=[],
            selected_property_types=[], selected_equipment_types=[],
            selected_equipment_access=[], selected_equipment_responsibility=[],
            selected_aircraft_safety=[], selected_aircraft_expenses=[],
            selected_vessel_safety=[], selected_vessel_financial=[],
            selected_specialist_items=[], selected_art_forms=[],
            # Multi-select cities initialization
            selected_prop_cities=[], selected_car_cities=[],
            selected_equip_cities=[], selected_air_cities=[],
            selected_vessel_cities=[], selected_intro_cities=[],
            # Specialists list initialization
            specialists_list=[],
            # Aircraft types multi-select
            selected_aircraft_types=[],
            # Vessel types multi-select
            selected_vessel_types=[]
        )

        intro_text = (
            "Hi luv! and welcome to JOYSEEKERS 🩵\n\n"
            "congrats! you’re lucky enough to be part of a closed community of successful pll who travel, do what they love, grow, and share resources and opportunities with each other.\n\n"
            "JOYSEEKERS is all about trust and sharing.\n\n"
            "here you can find friends around the world and access shared resources — from skills and introductions to specific circles to real estate, cars, and equipment.\n\n"
            "every resource is equal:\n"
            "1 resource = 1 credit.\n\n"
            "If someone uses what you share, you earn a credit to unlock something else in return.\n\n"
            "want to know how it works?\n"
            "check our community channel after you finish the questionnaire — the link will pop up automatically.\n\n"
            "to get started, just fill out a short questionnaire and add the resources you’re open to sharing.\n"
            "after that and short approval by me all sections of the community will be unlocked for you.\n\n"
            "glad to be here with you.\n"
            "stay joyful 🩵\n"
            "xxAnna\n\n"
            "🍒\n\n"
            "please complete the questionnaire carefully.\n"
            "9 sections, ~10 minutes.\n\n"
            "incomplete submissions are not reviewed and will not be granted access to the Community.\n\n"
            "the bot will send questions one by one — just reply in chat or choose the available options.\n\n"
            "you can update or change your information at any time by contacting our manager via direct messages @papacaralya"
        )
        await message.answer(intro_text)
        await message.answer("Please enter your name:", reply_markup=get_cancel_keyboard())
        await state.set_state(Registration.name)


@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return
    await state.update_data(name=message.text)

    # Initialize empty selection for main city
    await state.update_data(selected_main_cities=[])

    # We use inline keyboard for multi-selection, so we need to remove the Reply keyboard (Back button)
    # or keep it and handle text "Back".
    # But get_cities_select_keyboard is inline.
    # We send a message with the inline keyboard.
    # We can also keep the Reply "Back" button active if we want, but it's cleaner to use inline back.
    # Let's remove the Reply keyboard first to avoid confusion.
    await message.answer("Great! Now, please select the city (or cities) where you are usually located:", reply_markup=ReplyKeyboardRemove())
    await message.answer("Select cities:", reply_markup=get_cities_select_keyboard("main_city", "main_city_done", set(), "main_city_back"))
    await state.set_state(Registration.main_city)


@router.message(Registration.main_city, F.text)
async def process_main_city_text(message: Message, state: FSMContext):
    # This handler might catch text if user types instead of clicking
    # If it is "Back", we go back.
    if message.text == "🔙 Back":
        await state.set_state(Registration.name)
        await message.answer("Please enter your name:", reply_markup=get_cancel_keyboard())
        return

    # If they typed a city, we can accept it, but we prefer selection
    await message.answer("Please select your city from the list or press Done if you typed it (Wait, just use the buttons):", reply_markup=get_cities_select_keyboard("main_city", "main_city_done", set(), "main_city_back"))

@router.callback_query(Registration.main_city, F.data == "main_city_back")
async def back_from_main_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Please enter your name:", reply_markup=get_cancel_keyboard())
    await state.set_state(Registration.name)
    await callback.answer()

@router.callback_query(Registration.main_city, F.data.startswith("main_city:"))
async def select_main_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_main_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_main_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("main_city", "main_city_done", selected, "main_city_back"))
    await callback.answer()

@router.callback_query(Registration.main_city, F.data == "main_city_done")
async def finish_main_city(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_cities = data.get("selected_main_cities", [])

    if not selected_cities:
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    # Join cities for display/storage (comma separated)
    main_city_str = ", ".join(selected_cities)
    await state.update_data(main_city=main_city_str)

    await callback.message.delete() # Remove inline keyboard
    await callback.message.answer(
        "Tell us a bit about yourself (brief intro):\n\nFor example •Artist and community owner•",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.about)
    await callback.answer()


@router.message(Registration.about, F.text)
async def process_about(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await state.set_state(Registration.main_city)
        await message.answer("Great! Now, please enter the city where you are usually located:", reply_markup=get_cancel_keyboard())
        return
    await state.update_data(about=message.text)
    await message.answer("Please enter your Instagram username (or send '-' if you don't have one):", reply_markup=get_cancel_keyboard())
    await state.set_state(Registration.instagram)


@router.message(Registration.instagram, F.text)
async def process_instagram(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await state.set_state(Registration.about)
        await message.answer("Tell us a bit about yourself (brief intro):\n\nFor example •Artist and community owner•", reply_markup=get_cancel_keyboard())
        return
    instagram = message.text if message.text != "-" else ""
    await state.update_data(instagram=instagram)

    # We remove the keyboard for processing, but immediately show inline keyboard for next step.
    # The user asked for "Back" button on every question.
    # For inline keyboards, we implement "Back" in the keyboard itself.
    # We don't send ReplyKeyboardRemove because we want the user to be able to use standard keyboard if needed?
    # No, skills selection is inline.

    await message.answer("Processing...", reply_markup=ReplyKeyboardRemove())

    skills_intro = (
        "1|9 🩵 Skills and Knowledge\n\n"
        "Please provide information about the skills, knowledge, and professional abilities "
        "you are willing to share with the community.\n\n"
        "Each of us carries unique mastery. Here you can list the areas where you can:\n"
        "• give a thoughtful consultation\n"
        "• teach your skill or method\n"
        "• guide someone through a process\n"
        "• create or deliver a clear final result\n\n"
        "Select your Category of Expertise: You may select multiple options across different categories."
    )
    # No back button here because previous step was text input.
    # But wait, user might want to go back to Instagram input?
    # The current library setup for get_skill_categories_keyboard doesn't take back_callback.
    # We should add it.
    await message.answer(skills_intro, reply_markup=get_skill_categories_keyboard())
    await state.set_state(Registration.skill_category)


# --- Skills Section Handlers ---

@router.callback_query(Registration.skill_category, F.data.startswith("q_cat:"))
async def process_skill_category(callback: CallbackQuery, state: FSMContext):
    category_key = callback.data.split(":")[1]
    category_name = SKILL_CATEGORIES[category_key]["name"]
    await state.update_data(current_category=category_key)
    data = await state.get_data()
    selected_items = set(data.get("selected_skill_items", []))
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect specific skills/areas (you can select multiple):",
        reply_markup=get_skill_items_keyboard(category_key, selected_items)
    )
    await state.set_state(Registration.skill_items)
    await callback.answer()


@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))
async def process_skill_item_toggle(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    category_key = data.get("current_category")
    items_list = SKILL_CATEGORIES.get(category_key, {}).get("items", [])
    target_item = find_item_by_hash(items_list, item_hash)
    if target_item:
        selected_items = set(data.get("selected_skill_items", []))
        if target_item in selected_items:
            selected_items.remove(target_item)
        else:
            selected_items.add(target_item)
        await state.update_data(selected_skill_items=list(selected_items))
        await callback.message.edit_reply_markup(reply_markup=get_skill_items_keyboard(category_key, selected_items))
    await callback.answer()


@router.callback_query(Registration.skill_items, F.data == "q_back_cat")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Select your Category of Expertise: You may select multiple options across different categories.", reply_markup=get_skill_categories_keyboard())
    await state.set_state(Registration.skill_category)
    await callback.answer()


@router.callback_query(Registration.skill_items, F.data == "q_item_done")
async def finish_skill_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_skill_items", [])
    if not selected_items:
        await callback.answer("Please select at least one skill.", show_alert=True)
        return

    selected = set(data.get("selected_offer_formats", []))
    await callback.message.edit_text(
        "Formats You Offer\n\nSelect the formats in which you can share your expertise (you can select multiple):",
        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back")
    )
    await state.set_state(Registration.offer_formats)
    await callback.answer()

# Back from offer formats
@router.callback_query(Registration.offer_formats, F.data == "q_fmt_back")
async def back_from_offer_formats(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Select your Category of Expertise: You may select multiple options across different categories.", reply_markup=get_skill_categories_keyboard())
    await state.set_state(Registration.skill_category)
    await callback.answer()


@router.callback_query(Registration.offer_formats, F.data.startswith("q_fmt:"))
async def toggle_offer_format(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_offer_formats", []))
    target_item = find_item_by_hash(OFFER_FORMATS, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_offer_formats=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back"))
    await callback.answer()


@router.callback_query(Registration.offer_formats, F.data == "q_fmt_done")
async def finish_offer_formats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_offer_formats", [])
    if not selected_items:
        await callback.answer("Please select at least one format.", show_alert=True)
        return

    selected = set(data.get("selected_interaction_formats", []))
    await callback.message.edit_text(
        "Interaction Format\n\nHow do you prefer to interact with community members?",
        reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done", "q_int_back")
    )
    await state.set_state(Registration.interaction_format)
    await callback.answer()

@router.callback_query(Registration.interaction_format, F.data == "q_int_back")
async def back_from_interaction_format(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_offer_formats", []))
    await callback.message.edit_text(
        "Formats You Offer\n\nSelect the formats in which you can share your expertise (you can select multiple):",
        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back")
    )
    await state.set_state(Registration.offer_formats)
    await callback.answer()


@router.callback_query(Registration.interaction_format, F.data.startswith("q_int:"))
async def toggle_interaction_format(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_interaction_formats", []))
    target_item = find_item_by_hash(INTERACTION_FORMATS, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_interaction_formats=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done", "q_int_back"))
    await callback.answer()


@router.callback_query(Registration.interaction_format, F.data == "q_int_done")
async def finish_interaction_formats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_interaction_formats", [])
    if not selected_items:
        await callback.answer("Please select at least one interaction format.", show_alert=True)
        return

    selected = set(data.get("selected_result_types", []))
    await callback.message.edit_text(
        "Type of Result\n\nWhat kind of result can you deliver?",
        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back")
    )
    await state.set_state(Registration.result_type)
    await callback.answer()

@router.callback_query(Registration.result_type, F.data == "q_res_back")
async def back_from_result_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_interaction_formats", []))
    await callback.message.edit_text(
        "Interaction Format\n\nHow do you prefer to interact with community members?",
        reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done", "q_int_back")
    )
    await state.set_state(Registration.interaction_format)
    await callback.answer()


@router.callback_query(Registration.result_type, F.data.startswith("q_res:"))
async def toggle_result_type(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_result_types", []))
    target_item = find_item_by_hash(RESULT_TYPES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_result_types=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back"))
    await callback.answer()


@router.callback_query(Registration.result_type, F.data == "q_res_done")
async def finish_skills_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_result_types", [])
    if not selected_items:
        await callback.answer("Please select at least one result type.", show_alert=True)
        return

    # Move to Personal Introductions section
    intro_text = (
        "2|9 🩵 Personal Introductions to Key People\n\n"
        "In almost every life story, there is a moment when someone opened a door for us.\n\n"
        "Here, you can describe the key people in your orbit — founders, creators, innovators, "
        "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"
        "Sharing information about them does not commit you to making an introduction."
    )
    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))
    await state.set_state(Registration.intro_section)
    await callback.answer()

@router.callback_query(Registration.intro_section, F.data == "intro_sec_back")
async def back_to_result_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_result_types", []))
    await callback.message.edit_text(
        "Type of Result\n\nWhat kind of result can you deliver?",
        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back")
    )
    await state.set_state(Registration.result_type)
    await callback.answer()


# --- Personal Introductions Section ---

@router.callback_query(Registration.intro_section, F.data == "intro_skip")
async def skip_intro_section(callback: CallbackQuery, state: FSMContext):
    # Move to Real Estate section
    real_estate_text = (
        "3|9 🩵 Real Estate\n\n"
        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "
        "to host another resident in a separate room — this is where you can share it with the community.\n\n"
        "Please list only the properties you are willing to share free of charge."
    )
    await callback.message.edit_text(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))
    await state.set_state(Registration.real_estate_section)
    await callback.answer()


@router.callback_query(Registration.intro_section, F.data == "intro_start")
async def start_intro_section(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Select the category of people you can introduce:",
        reply_markup=get_category_keyboard(INTRO_CATEGORIES, "intro_cat", "intro_cat_back")
    )
    await state.set_state(Registration.intro_category)
    await callback.answer()

@router.callback_query(Registration.intro_category, F.data == "intro_cat_back")
async def back_to_intro_section(callback: CallbackQuery, state: FSMContext):
    intro_text = (
        "2|9 🩵 Personal Introductions to Key People\n\n"
        "In almost every life story, there is a moment when someone opened a door for us.\n\n"
        "Here, you can describe the key people in your orbit — founders, creators, innovators, "
        "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"
        "Sharing information about them does not commit you to making an introduction."
    )
    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))
    await state.set_state(Registration.intro_section)
    await callback.answer()


@router.callback_query(Registration.intro_category, F.data.startswith("intro_cat:"))
async def process_intro_category(callback: CallbackQuery, state: FSMContext):
    category_key = callback.data.split(":")[1]
    await state.update_data(current_intro_category=category_key)
    data = await state.get_data()
    selected = set(data.get("selected_intro_items", []))
    category_name = INTRO_CATEGORIES[category_key]["name"]
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the people you can introduce:",
        reply_markup=get_category_items_keyboard(category_key, INTRO_CATEGORIES, selected, "intro_item", "intro_item_done", "intro_back_cat")
    )
    await state.set_state(Registration.intro_items)
    await callback.answer()


@router.callback_query(Registration.intro_items, F.data.startswith("intro_item:"))
async def toggle_intro_item(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    category_key = data.get("current_intro_category")
    items_list = INTRO_CATEGORIES.get(category_key, {}).get("items", [])
    target_item = find_item_by_hash(items_list, item_hash)
    if target_item:
        selected = set(data.get("selected_intro_items", []))
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_intro_items=list(selected))
        await callback.message.edit_reply_markup(
            reply_markup=get_category_items_keyboard(category_key, INTRO_CATEGORIES, selected, "intro_item", "intro_item_done", "intro_back_cat")
        )
    await callback.answer()


@router.callback_query(Registration.intro_items, F.data == "intro_back_cat")
async def back_to_intro_categories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Select the category of people you can introduce:", reply_markup=get_category_keyboard(INTRO_CATEGORIES, "intro_cat", "intro_cat_back"))
    await state.set_state(Registration.intro_category)
    await callback.answer()


@router.callback_query(Registration.intro_items, F.data == "intro_item_done")
async def finish_intro_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_intro_items", []):
         await callback.answer("Please select at least one item.", show_alert=True)
         return

    selected = set(data.get("selected_intro_cities", []))
    await callback.message.edit_text("Select your location:", reply_markup=get_cities_select_keyboard("intro_city", "intro_city_done", selected, "intro_city_back"))
    await state.set_state(Registration.intro_location)
    await callback.answer()

@router.callback_query(Registration.intro_location, F.data == "intro_city_back")
async def back_from_intro_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Select the category of people you can introduce:", reply_markup=get_category_keyboard(INTRO_CATEGORIES, "intro_cat", "intro_cat_back"))
    await state.set_state(Registration.intro_category)
    await callback.answer()


@router.callback_query(Registration.intro_location, F.data.startswith("intro_city:"))
async def select_intro_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_intro_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_intro_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("intro_city", "intro_city_done", selected, "intro_city_back"))
    await callback.answer()


@router.callback_query(Registration.intro_location, F.data == "intro_city_done")
async def finish_intro_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_intro_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    selected = set(data.get("selected_intro_formats", []))
    await callback.message.edit_text(
        "Intro Format\n\nSpecify the format of introduction you are comfortable with:",
        reply_markup=get_multiselect_keyboard(INTRO_FORMATS, selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back")
    )
    await state.set_state(Registration.intro_format)
    await callback.answer()

@router.callback_query(Registration.intro_format, F.data == "intro_fmt_back")
async def back_from_intro_format(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_intro_cities", []))
    await callback.message.edit_text("Select your location:", reply_markup=get_cities_select_keyboard("intro_city", "intro_city_done", selected, "intro_city_back"))
    await state.set_state(Registration.intro_location)
    await callback.answer()


@router.callback_query(Registration.intro_format, F.data.startswith("intro_fmt:"))
async def toggle_intro_format(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_intro_formats", []))
    target_item = find_item_by_hash(INTRO_FORMATS, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_intro_formats=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(INTRO_FORMATS, selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back"))
    await callback.answer()


@router.callback_query(Registration.intro_format, F.data == "intro_fmt_done")
async def finish_intro_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_intro_formats", []):
        await callback.answer("Please select at least one format.", show_alert=True)
        return

    # Progress message
    await callback.message.answer("wooo-hoo! \nyou’re doing great — already completed a third! 👏🏻 just a little more to go.")

    # Move to Real Estate section
    real_estate_text = (
        "3|9 🩵 Real Estate\n\n"
        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "
        "to host another resident in a separate room — this is where you can share it with the community.\n\n"
        "Please list only the properties you are willing to share free of charge."
    )
    await callback.message.answer(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))
    await state.set_state(Registration.real_estate_section)
    await callback.answer()

@router.callback_query(Registration.real_estate_section, F.data == "re_sec_back")
async def back_from_re_section(callback: CallbackQuery, state: FSMContext):
    # Go back to intro section last step
    data = await state.get_data()
    selected = set(data.get("selected_intro_formats", []))
    await callback.message.edit_text(
        "Intro Format\n\nSpecify the format of introduction you are comfortable with:",
        reply_markup=get_multiselect_keyboard(INTRO_FORMATS, selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back")
    )
    await state.set_state(Registration.intro_format)
    await callback.answer()


# --- Real Estate Section ---

@router.callback_query(Registration.real_estate_section, F.data == "realestate_skip")
async def skip_realestate_section(callback: CallbackQuery, state: FSMContext):
    cars_text = (
        "4|9 🩵 Cars and other vehicles\n\n"
        "Please provide information about the cars you are willing to make available to community residents.\n\n"
        "By sharing your car, you're offering more than just a vehicle — you're giving someone the chance "
        "to experience freedom, explore, and create new memories."
    )
    await callback.message.edit_text(cars_text, reply_markup=get_section_intro_keyboard("cars_start", "cars_skip", "cars_sec_back"))
    await state.set_state(Registration.cars_section)
    await callback.answer()


@router.callback_query(Registration.real_estate_section, F.data == "realestate_start")
async def start_realestate_section(callback: CallbackQuery, state: FSMContext):
    # City first
    data = await state.get_data()
    selected = set(data.get("selected_prop_cities", []))
    await callback.message.edit_text(
        "Location\n\nSelect your property location:",
        reply_markup=get_cities_select_keyboard("prop_city", "prop_city_done", selected, "prop_city_back")
    )
    await state.set_state(Registration.property_location)
    await callback.answer()

@router.callback_query(Registration.property_location, F.data == "prop_city_back")
async def back_from_prop_city(callback: CallbackQuery, state: FSMContext):
    real_estate_text = (
        "3|9 🩵 Real Estate\n\n"
        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "
        "to host another resident in a separate room — this is where you can share it with the community.\n\n"
        "Please list only the properties you are willing to share free of charge."
    )
    await callback.message.edit_text(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))
    await state.set_state(Registration.real_estate_section)
    await callback.answer()


@router.callback_query(Registration.property_location, F.data.startswith("prop_city:"))
async def select_property_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_prop_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_prop_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("prop_city", "prop_city_done", selected, "prop_city_back"))
    await callback.answer()


@router.callback_query(Registration.property_location, F.data == "prop_city_done")
async def finish_property_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_prop_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    selected = set(data.get("selected_property_types", []))
    await callback.message.edit_text(
        "Type of Property\n\nPlease select:",
        reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back")
    )
    await state.set_state(Registration.property_type)
    await callback.answer()

@router.callback_query(Registration.property_type, F.data == "prop_type_back")
async def back_from_prop_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_prop_cities", []))
    await callback.message.edit_text(
        "Location\n\nSelect your property location:",
        reply_markup=get_cities_select_keyboard("prop_city", "prop_city_done", selected, "prop_city_back")
    )
    await state.set_state(Registration.property_location)
    await callback.answer()


@router.callback_query(Registration.property_type, F.data.startswith("prop_type:"))
async def toggle_property_type(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_property_types", []))
    target_item = find_item_by_hash(PROPERTY_TYPES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_property_types=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back"))
    await callback.answer()


@router.callback_query(Registration.property_type, F.data == "prop_type_done")
async def finish_property_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_property_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    await callback.message.edit_text(
        "Usage Format\n\nChoose the suitable option:",
        reply_markup=get_single_select_keyboard(PROPERTY_USAGE_FORMAT, "prop_usage", "prop_usage_back")
    )
    await state.set_state(Registration.property_usage)
    await callback.answer()

@router.callback_query(Registration.property_usage, F.data == "prop_usage_back")
async def back_from_prop_usage(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_property_types", []))
    await callback.message.edit_text(
        "Type of Property\n\nPlease select:",
        reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back")
    )
    await state.set_state(Registration.property_type)
    await callback.answer()


@router.callback_query(Registration.property_usage, F.data.startswith("prop_usage:"))
async def select_property_usage(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(PROPERTY_USAGE_FORMAT, item_hash)
    if target_item:
        await state.update_data(property_usage=target_item)
    await callback.message.edit_text(
        "Duration of Use\n\nAvailable options:",
        reply_markup=get_single_select_keyboard(PROPERTY_DURATION, "prop_dur", "prop_dur_back")
    )
    await state.set_state(Registration.property_duration)
    await callback.answer()

@router.callback_query(Registration.property_duration, F.data == "prop_dur_back")
async def back_from_prop_duration(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Usage Format\n\nChoose the suitable option:",
        reply_markup=get_single_select_keyboard(PROPERTY_USAGE_FORMAT, "prop_usage", "prop_usage_back")
    )
    await state.set_state(Registration.property_usage)
    await callback.answer()


@router.callback_query(Registration.property_duration, F.data.startswith("prop_dur:"))
async def select_property_duration(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(PROPERTY_DURATION, item_hash)
    if target_item:
        await state.update_data(property_duration=target_item)
    await callback.message.edit_text(
        "Capacity\n\nNumber of people who can comfortably stay:",
        reply_markup=get_single_select_keyboard(PROPERTY_CAPACITY, "prop_cap", "prop_cap_back")
    )
    await state.set_state(Registration.property_capacity)
    await callback.answer()

@router.callback_query(Registration.property_capacity, F.data == "prop_cap_back")
async def back_from_prop_capacity(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Duration of Use\n\nAvailable options:",
        reply_markup=get_single_select_keyboard(PROPERTY_DURATION, "prop_dur", "prop_dur_back")
    )
    await state.set_state(Registration.property_duration)
    await callback.answer()


@router.callback_query(Registration.property_capacity, F.data.startswith("prop_cap:"))
async def select_property_capacity(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(PROPERTY_CAPACITY, item_hash)
    if target_item:
        await state.update_data(property_capacity=target_item)

    # Move to Cars section
    cars_text = (
        "4|9 🩵 Cars and other vehicles\n\n"
        "Please provide information about the cars you are willing to make available to community residents.\n\n"
        "By sharing your car, you're offering more than just a vehicle — you're giving someone the chance "
        "to experience freedom, explore, and create new memories."
    )
    await callback.message.edit_text(cars_text, reply_markup=get_section_intro_keyboard("cars_start", "cars_skip", "cars_sec_back"))
    await state.set_state(Registration.cars_section)
    await callback.answer()

@router.callback_query(Registration.cars_section, F.data == "cars_sec_back")
async def back_from_cars_section(callback: CallbackQuery, state: FSMContext):
    # Back to Property Capacity
    await callback.message.edit_text(
        "Capacity\n\nNumber of people who can comfortably stay:",
        reply_markup=get_single_select_keyboard(PROPERTY_CAPACITY, "prop_cap", "prop_cap_back")
    )
    await state.set_state(Registration.property_capacity)
    await callback.answer()


# --- Cars Section ---

@router.callback_query(Registration.cars_section, F.data == "cars_skip")
async def skip_cars_section(callback: CallbackQuery, state: FSMContext):
    equipment_text = (
        "5|9 🩵 Equipment\n\n"
        "Please provide information about the equipment you are willing to make available to community residents.\n\n"
        "By providing clear details about the resources you're open to sharing, you help the community grow stronger."
    )
    await callback.message.edit_text(equipment_text, reply_markup=get_section_intro_keyboard("equipment_start", "equipment_skip", "equip_sec_back"))
    await state.set_state(Registration.equipment_section)
    await callback.answer()


@router.callback_query(Registration.cars_section, F.data == "cars_start")
async def start_cars_section(callback: CallbackQuery, state: FSMContext):
    # City first
    data = await state.get_data()
    selected = set(data.get("selected_car_cities", []))
    await callback.message.edit_text(
        "Location\n\nSelect your vehicle location:",
        reply_markup=get_cities_select_keyboard("car_city", "car_city_done", selected, "car_city_back")
    )
    await state.set_state(Registration.car_location)
    await callback.answer()

@router.callback_query(Registration.car_location, F.data == "car_city_back")
async def back_from_car_city(callback: CallbackQuery, state: FSMContext):
    cars_text = (
        "4|9 🩵 Cars and other vehicles\n\n"
        "Please provide information about the cars you are willing to make available to community residents.\n\n"
        "By sharing your car, you're offering more than just a vehicle — you're giving someone the chance "
        "to experience freedom, explore, and create new memories."
    )
    await callback.message.edit_text(cars_text, reply_markup=get_section_intro_keyboard("cars_start", "cars_skip", "cars_sec_back"))
    await state.set_state(Registration.cars_section)
    await callback.answer()


@router.callback_query(Registration.car_location, F.data.startswith("car_city:"))
async def select_car_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_car_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_car_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("car_city", "car_city_done", selected, "car_city_back"))
    await callback.answer()


@router.callback_query(Registration.car_location, F.data == "car_city_done")
async def finish_car_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_car_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    await callback.message.delete()
    await callback.message.answer(
        "Vehicle Brand, Model & Year\n\nPlease type the info (e.g., Toyota Fortuner 2021):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.car_info)
    await callback.answer()


@router.message(Registration.car_info, F.text)
async def process_car_info(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        # Go back to location
        data = await state.get_data()
        selected = set(data.get("selected_car_cities", []))
        await message.answer("Location\n\nSelect your vehicle location:", reply_markup=get_cities_select_keyboard("car_city", "car_city_done", selected, "car_city_back"))
        await state.set_state(Registration.car_location)
        return

    await state.update_data(car_info=message.text)

    # Remove keyboard for inline next
    await message.answer("Processing...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Usage Conditions\n\nChoose one:",
        reply_markup=get_single_select_keyboard(CAR_USAGE_CONDITIONS, "car_usage", "car_usage_back")
    )
    await state.set_state(Registration.car_usage)

@router.callback_query(Registration.car_usage, F.data == "car_usage_back")
async def back_from_car_usage(callback: CallbackQuery, state: FSMContext):
    # Back to text input is tricky with callback.
    # We send a message asking for input again.
    await callback.message.delete()
    await callback.message.answer(
        "Vehicle Brand, Model & Year\n\nPlease type the info (e.g., Toyota Fortuner 2021):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.car_info)
    await callback.answer()


@router.callback_query(Registration.car_usage, F.data.startswith("car_usage:"))
async def select_car_usage(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(CAR_USAGE_CONDITIONS, item_hash)
    if target_item:
        await state.update_data(car_usage=target_item)
    await callback.message.edit_text(
        "Duration of Use\n\nAvailable options:",
        reply_markup=get_single_select_keyboard(CAR_DURATION, "car_dur", "car_dur_back")
    )
    await state.set_state(Registration.car_duration)
    await callback.answer()

@router.callback_query(Registration.car_duration, F.data == "car_dur_back")
async def back_from_car_duration(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Usage Conditions\n\nChoose one:",
        reply_markup=get_single_select_keyboard(CAR_USAGE_CONDITIONS, "car_usage", "car_usage_back")
    )
    await state.set_state(Registration.car_usage)


@router.callback_query(Registration.car_duration, F.data.startswith("car_dur:"))
async def select_car_duration(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(CAR_DURATION, item_hash)
    if target_item:
        await state.update_data(car_duration=target_item)
    data = await state.get_data()
    selected = set(data.get("selected_car_conditions", []))
    await callback.message.edit_text(
        "Conditions:",
        reply_markup=get_multiselect_keyboard(CAR_CONDITIONS, selected, "car_cond", "car_cond_done", "car_cond_back")
    )
    await state.set_state(Registration.car_conditions)
    await callback.answer()

@router.callback_query(Registration.car_conditions, F.data == "car_cond_back")
async def back_from_car_conditions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Duration of Use\n\nAvailable options:",
        reply_markup=get_single_select_keyboard(CAR_DURATION, "car_dur", "car_dur_back")
    )
    await state.set_state(Registration.car_duration)
    await callback.answer()


@router.callback_query(Registration.car_conditions, F.data.startswith("car_cond:"))
async def toggle_car_condition(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_car_conditions", []))
    target_item = find_item_by_hash(CAR_CONDITIONS, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_car_conditions=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(CAR_CONDITIONS, selected, "car_cond", "car_cond_done", "car_cond_back"))
    await callback.answer()


@router.callback_query(Registration.car_conditions, F.data == "car_cond_done")
async def finish_car_conditions(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_car_conditions", []):
        await callback.answer("Please select at least one condition.", show_alert=True)
        return

    await callback.message.edit_text(
        "Maximum Passengers:",
        reply_markup=get_single_select_keyboard(CAR_PASSENGERS, "car_pass", "car_pass_back")
    )
    await state.set_state(Registration.car_passengers)
    await callback.answer()

@router.callback_query(Registration.car_passengers, F.data == "car_pass_back")
async def back_from_car_passengers(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_car_conditions", []))
    await callback.message.edit_text(
        "Conditions:",
        reply_markup=get_multiselect_keyboard(CAR_CONDITIONS, selected, "car_cond", "car_cond_done", "car_cond_back")
    )
    await state.set_state(Registration.car_conditions)
    await callback.answer()


@router.callback_query(Registration.car_passengers, F.data.startswith("car_pass:"))
async def select_car_passengers(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(CAR_PASSENGERS, item_hash)
    if target_item:
        await state.update_data(car_passengers=target_item)

    # Move to Equipment section
    equipment_text = (
        "5|9 🩵 Equipment\n\n"
        "Please provide information about the equipment you are willing to make available to community residents.\n\n"
        "By providing clear details about the resources you're open to sharing, you help the community grow stronger."
    )
    await callback.message.edit_text(equipment_text, reply_markup=get_section_intro_keyboard("equipment_start", "equipment_skip", "equip_sec_back"))
    await state.set_state(Registration.equipment_section)
    await callback.answer()

@router.callback_query(Registration.equipment_section, F.data == "equip_sec_back")
async def back_from_equip_section(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Maximum Passengers:",
        reply_markup=get_single_select_keyboard(CAR_PASSENGERS, "car_pass", "car_pass_back")
    )
    await state.set_state(Registration.car_passengers)
    await callback.answer()


# --- Equipment Section ---

@router.callback_query(Registration.equipment_section, F.data == "equipment_skip")
async def skip_equipment_section(callback: CallbackQuery, state: FSMContext):
    aircraft_text = (
        "6|9 🩵 Air Transport\n\n"
        "Please provide information about the aircraft you are willing to make available to community residents.\n\n"
        "By opening access to such a unique asset, you take a special role within the community — "
        "inspiring others, elevating shared values, and creating moments that simply cannot happen without you."
    )
    await callback.message.edit_text(aircraft_text, reply_markup=get_section_intro_keyboard("aircraft_start", "aircraft_skip", "air_sec_back"))
    await state.set_state(Registration.aircraft_section)
    await callback.answer()


@router.callback_query(Registration.equipment_section, F.data == "equipment_start")
async def start_equipment_section(callback: CallbackQuery, state: FSMContext):
    # City first
    data = await state.get_data()
    selected = set(data.get("selected_equip_cities", []))
    await callback.message.edit_text(
        "Location\n\nSelect equipment location:",
        reply_markup=get_cities_select_keyboard("equip_city", "equip_city_done", selected, "equip_city_back")
    )
    await state.set_state(Registration.equipment_location)
    await callback.answer()

@router.callback_query(Registration.equipment_location, F.data == "equip_city_back")
async def back_from_equip_location(callback: CallbackQuery, state: FSMContext):
    equipment_text = (
        "5|9 🩵 Equipment\n\n"
        "Please provide information about the equipment you are willing to make available to community residents.\n\n"
        "By providing clear details about the resources you're open to sharing, you help the community grow stronger."
    )
    await callback.message.edit_text(equipment_text, reply_markup=get_section_intro_keyboard("equipment_start", "equipment_skip", "equip_sec_back"))
    await state.set_state(Registration.equipment_section)
    await callback.answer()


@router.callback_query(Registration.equipment_location, F.data.startswith("equip_city:"))
async def select_equipment_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_equip_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_equip_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("equip_city", "equip_city_done", selected, "equip_city_back"))
    await callback.answer()


@router.callback_query(Registration.equipment_location, F.data == "equip_city_done")
async def finish_equipment_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equip_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    selected = set(data.get("selected_equipment_types", []))
    await callback.message.edit_text(
        "Types of Equipment You Can Share\n\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back")
    )
    await state.set_state(Registration.equipment_types)
    await callback.answer()

@router.callback_query(Registration.equipment_types, F.data == "equip_type_back")
async def back_from_equip_types(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equip_cities", []))
    await callback.message.edit_text(
        "Location\n\nSelect equipment location:",
        reply_markup=get_cities_select_keyboard("equip_city", "equip_city_done", selected, "equip_city_back")
    )
    await state.set_state(Registration.equipment_location)
    await callback.answer()


@router.callback_query(Registration.equipment_types, F.data.startswith("equip_type:"))
async def toggle_equipment_type(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_equipment_types", []))
    target_item = find_item_by_hash(EQUIPMENT_TYPES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_equipment_types=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back"))
    await callback.answer()


@router.callback_query(Registration.equipment_types, F.data == "equip_type_done")
async def finish_equipment_types(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equipment_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    selected = set(data.get("selected_equipment_access", []))
    await callback.message.edit_text(
        "Equipment Access Format\n\nChoose one or multiple:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_ACCESS_FORMAT, selected, "equip_acc", "equip_acc_done", "equip_acc_back")
    )
    await state.set_state(Registration.equipment_access)
    await callback.answer()

@router.callback_query(Registration.equipment_access, F.data == "equip_acc_back")
async def back_from_equip_access(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equipment_types", []))
    await callback.message.edit_text(
        "Types of Equipment You Can Share\n\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back")
    )
    await state.set_state(Registration.equipment_types)
    await callback.answer()


@router.callback_query(Registration.equipment_access, F.data.startswith("equip_acc:"))
async def toggle_equipment_access(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_equipment_access", []))
    target_item = find_item_by_hash(EQUIPMENT_ACCESS_FORMAT, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_equipment_access=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(EQUIPMENT_ACCESS_FORMAT, selected, "equip_acc", "equip_acc_done", "equip_acc_back"))
    await callback.answer()


@router.callback_query(Registration.equipment_access, F.data == "equip_acc_done")
async def finish_equipment_access(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equipment_access", []):
        await callback.answer("Please select at least one format.", show_alert=True)
        return

    await callback.message.edit_text(
        "Duration of Use:",
        reply_markup=get_single_select_keyboard(EQUIPMENT_DURATION, "equip_dur", "equip_dur_back")
    )
    await state.set_state(Registration.equipment_duration)
    await callback.answer()

@router.callback_query(Registration.equipment_duration, F.data == "equip_dur_back")
async def back_from_equip_duration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equipment_access", []))
    await callback.message.edit_text(
        "Equipment Access Format\n\nChoose one or multiple:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_ACCESS_FORMAT, selected, "equip_acc", "equip_acc_done", "equip_acc_back")
    )
    await state.set_state(Registration.equipment_access)
    await callback.answer()


@router.callback_query(Registration.equipment_duration, F.data.startswith("equip_dur:"))
async def select_equipment_duration(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(EQUIPMENT_DURATION, item_hash)
    if target_item:
        await state.update_data(equipment_duration=target_item)
    data = await state.get_data()
    selected = set(data.get("selected_equipment_responsibility", []))
    await callback.message.edit_text(
        "Responsibility and Safety:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_RESPONSIBILITY, selected, "equip_resp", "equip_resp_done", "equip_resp_back")
    )
    await state.set_state(Registration.equipment_responsibility)
    await callback.answer()

@router.callback_query(Registration.equipment_responsibility, F.data == "equip_resp_back")
async def back_from_equip_resp(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Duration of Use:",
        reply_markup=get_single_select_keyboard(EQUIPMENT_DURATION, "equip_dur", "equip_dur_back")
    )
    await state.set_state(Registration.equipment_duration)
    await callback.answer()


@router.callback_query(Registration.equipment_responsibility, F.data.startswith("equip_resp:"))
async def toggle_equipment_responsibility(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_equipment_responsibility", []))
    target_item = find_item_by_hash(EQUIPMENT_RESPONSIBILITY, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_equipment_responsibility=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(EQUIPMENT_RESPONSIBILITY, selected, "equip_resp", "equip_resp_done", "equip_resp_back"))
    await callback.answer()


@router.callback_query(Registration.equipment_responsibility, F.data == "equip_resp_done")
async def finish_equipment_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equipment_responsibility", []):
        await callback.answer("Please select at least one option.", show_alert=True)
        return

    aircraft_text = (
        "6|9 🩵 Air Transport\n\n"
        "Please provide information about the aircraft you are willing to make available to community residents.\n\n"
        "By opening access to such a unique asset, you take a special role within the community — "
        "inspiring others, elevating shared values, and creating moments that simply cannot happen without you."
    )
    await callback.message.edit_text(aircraft_text, reply_markup=get_section_intro_keyboard("aircraft_start", "aircraft_skip", "air_sec_back"))
    await state.set_state(Registration.aircraft_section)
    await callback.answer()

@router.callback_query(Registration.aircraft_section, F.data == "air_sec_back")
async def back_from_air_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equipment_responsibility", []))
    await callback.message.edit_text(
        "Responsibility and Safety:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_RESPONSIBILITY, selected, "equip_resp", "equip_resp_done", "equip_resp_back")
    )
    await state.set_state(Registration.equipment_responsibility)
    await callback.answer()


# --- Air Transport Section ---

@router.callback_query(Registration.aircraft_section, F.data == "aircraft_skip")
async def skip_aircraft_section(callback: CallbackQuery, state: FSMContext, db: Database):
    await callback.message.answer("complete the questionnaire carefully and you’ll receive 1 point to exchange within the community 🩵")

    vessel_text = (
        "7|9 🩵 Water Transport / Vessels\n\n"
        "Please provide information about the vessels you are willing to make available to community residents.\n\n"
        "We don't measure value in feet, engines, or length. What we share here is not \"status\" — "
        "but experiences, freedom and the joy of being on the water together."
    )
    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))
    await state.set_state(Registration.vessel_section)
    await callback.answer()


@router.callback_query(Registration.aircraft_section, F.data == "aircraft_start")
async def start_aircraft_section(callback: CallbackQuery, state: FSMContext):
    # City first
    data = await state.get_data()
    selected = set(data.get("selected_air_cities", []))
    await callback.message.edit_text("Location\n\nSelect aircraft location:", reply_markup=get_cities_select_keyboard("air_city", "air_city_done", selected, "air_city_back"))
    await state.set_state(Registration.aircraft_location)
    await callback.answer()

@router.callback_query(Registration.aircraft_location, F.data == "air_city_back")
async def back_from_air_city(callback: CallbackQuery, state: FSMContext):
    aircraft_text = (
        "6|9 🩵 Air Transport\n\n"
        "Please provide information about the aircraft you are willing to make available to community residents.\n\n"
        "By opening access to such a unique asset, you take a special role within the community — "
        "inspiring others, elevating shared values, and creating moments that simply cannot happen without you."
    )
    await callback.message.edit_text(aircraft_text, reply_markup=get_section_intro_keyboard("aircraft_start", "aircraft_skip", "air_sec_back"))
    await state.set_state(Registration.aircraft_section)
    await callback.answer()


@router.callback_query(Registration.aircraft_location, F.data.startswith("air_city:"))
async def select_aircraft_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_air_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_air_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("air_city", "air_city_done", selected, "air_city_back"))
    await callback.answer()


@router.callback_query(Registration.aircraft_location, F.data == "air_city_done")
async def finish_aircraft_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_air_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    # Multiselect for aircraft type
    selected = set(data.get("selected_aircraft_types", []))
    await callback.message.edit_text(
        "Type of Aircraft\n\nSelect:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back")
    )
    await state.set_state(Registration.aircraft_type)
    await callback.answer()

@router.callback_query(Registration.aircraft_type, F.data == "air_type_back")
async def back_from_air_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_air_cities", []))
    await callback.message.edit_text("Location\n\nSelect aircraft location:", reply_markup=get_cities_select_keyboard("air_city", "air_city_done", selected, "air_city_back"))
    await state.set_state(Registration.aircraft_location)
    await callback.answer()


@router.callback_query(Registration.aircraft_type, F.data.startswith("air_type:"))
async def toggle_aircraft_type(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_types", []))
    target_item = find_item_by_hash(AIRCRAFT_TYPES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_aircraft_types=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back"))
    await callback.answer()


@router.callback_query(Registration.aircraft_type, F.data == "air_type_done")
async def finish_aircraft_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_aircraft_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    await callback.message.edit_text(
        "Usage Format:",
        reply_markup=get_single_select_keyboard(AIRCRAFT_USAGE_FORMAT, "air_usage", "air_usage_back")
    )
    await state.set_state(Registration.aircraft_usage)
    await callback.answer()

@router.callback_query(Registration.aircraft_usage, F.data == "air_usage_back")
async def back_from_air_usage(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_types", []))
    await callback.message.edit_text(
        "Type of Aircraft\n\nSelect:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back")
    )
    await state.set_state(Registration.aircraft_type)
    await callback.answer()


@router.callback_query(Registration.aircraft_usage, F.data.startswith("air_usage:"))
async def select_aircraft_usage(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(AIRCRAFT_USAGE_FORMAT, item_hash)
    if target_item:
        await state.update_data(aircraft_usage=target_item)
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_safety", []))
    await callback.message.edit_text(
        "Safety and Insurance:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_SAFETY, selected, "air_safe", "air_safe_done", "air_safe_back")
    )
    await state.set_state(Registration.aircraft_safety)
    await callback.answer()

@router.callback_query(Registration.aircraft_safety, F.data == "air_safe_back")
async def back_from_air_safety(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Usage Format:",
        reply_markup=get_single_select_keyboard(AIRCRAFT_USAGE_FORMAT, "air_usage", "air_usage_back")
    )
    await state.set_state(Registration.aircraft_usage)
    await callback.answer()


@router.callback_query(Registration.aircraft_safety, F.data.startswith("air_safe:"))
async def toggle_aircraft_safety(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_safety", []))
    target_item = find_item_by_hash(AIRCRAFT_SAFETY, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_aircraft_safety=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(AIRCRAFT_SAFETY, selected, "air_safe", "air_safe_done", "air_safe_back"))
    await callback.answer()


@router.callback_query(Registration.aircraft_safety, F.data == "air_safe_done")
async def finish_aircraft_safety(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_aircraft_safety", []):
        await callback.answer("Please select at least one option.", show_alert=True)
        return

    selected = set(data.get("selected_aircraft_expenses", []))
    await callback.message.edit_text(
        "Expense Coverage:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_EXPENSES, selected, "air_exp", "air_exp_done", "air_exp_back")
    )
    await state.set_state(Registration.aircraft_expenses)
    await callback.answer()

@router.callback_query(Registration.aircraft_expenses, F.data == "air_exp_back")
async def back_from_air_expenses(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_safety", []))
    await callback.message.edit_text(
        "Safety and Insurance:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_SAFETY, selected, "air_safe", "air_safe_done", "air_safe_back")
    )
    await state.set_state(Registration.aircraft_safety)
    await callback.answer()


@router.callback_query(Registration.aircraft_expenses, F.data.startswith("air_exp:"))
async def toggle_aircraft_expenses(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_expenses", []))
    target_item = find_item_by_hash(AIRCRAFT_EXPENSES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_aircraft_expenses=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(AIRCRAFT_EXPENSES, selected, "air_exp", "air_exp_done", "air_exp_back"))
    await callback.answer()


@router.callback_query(Registration.aircraft_expenses, F.data == "air_exp_done")
async def finish_aircraft_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_aircraft_expenses", []):
        await callback.answer("Please select at least one option.", show_alert=True)
        return

    await callback.message.answer("complete the questionnaire carefully and you’ll receive 1 point to exchange within the community 🩵")

    vessel_text = (
        "7|9 🩵 Water Transport / Vessels\n\n"
        "Please provide information about the vessels you are willing to make available to community residents.\n\n"
        "We don't measure value in feet, engines, or length. What we share here is not \"status\" — "
        "but experiences, freedom and the joy of being on the water together."
    )
    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))
    await state.set_state(Registration.vessel_section)
    await callback.answer()

@router.callback_query(Registration.vessel_section, F.data == "vessel_sec_back")
async def back_from_vessel_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_expenses", []))
    await callback.message.edit_text(
        "Expense Coverage:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_EXPENSES, selected, "air_exp", "air_exp_done", "air_exp_back")
    )
    await state.set_state(Registration.aircraft_expenses)
    await callback.answer()


# --- Water Transport Section ---

@router.callback_query(Registration.vessel_section, F.data == "vessel_skip")
async def skip_vessel_section(callback: CallbackQuery, state: FSMContext):
    specialist_text = (
        "8|9 🩵 Specialists\n\n"
        "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "
        "brought clarity, or simply made life easier.\n\n"
        "Please list only those specialists you have personally worked with and can genuinely vouch for."
    )
    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
    await state.set_state(Registration.specialist_section)
    await callback.answer()


@router.callback_query(Registration.vessel_section, F.data == "vessel_start")
async def start_vessel_section(callback: CallbackQuery, state: FSMContext):
    # City first
    data = await state.get_data()
    selected = set(data.get("selected_vessel_cities", []))
    await callback.message.edit_text("Location and Sailing Area:", reply_markup=get_cities_select_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))
    await state.set_state(Registration.vessel_location)
    await callback.answer()

@router.callback_query(Registration.vessel_location, F.data == "vessel_city_back")
async def back_from_vessel_location(callback: CallbackQuery, state: FSMContext):
    vessel_text = (
        "7|9 🩵 Water Transport / Vessels\n\n"
        "Please provide information about the vessels you are willing to make available to community residents.\n\n"
        "We don't measure value in feet, engines, or length. What we share here is not \"status\" — "
        "but experiences, freedom and the joy of being on the water together."
    )
    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))
    await state.set_state(Registration.vessel_section)
    await callback.answer()


@router.callback_query(Registration.vessel_location, F.data.startswith("vessel_city:"))
async def select_vessel_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        data = await state.get_data()
        selected = set(data.get("selected_vessel_cities", []))
        if city in selected:
            selected.remove(city)
        else:
            selected.add(city)
        await state.update_data(selected_vessel_cities=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_cities_select_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))
    await callback.answer()


@router.callback_query(Registration.vessel_location, F.data == "vessel_city_done")
async def finish_vessel_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_vessel_cities", []):
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    # Updated: Multiselect for Vessel types
    selected = set(data.get("selected_vessel_types", []))
    await callback.message.edit_text(
        "Type of Vessel\n\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back")
    )
    await state.set_state(Registration.vessel_type)
    await callback.answer()

@router.callback_query(Registration.vessel_type, F.data == "vessel_type_back")
async def back_from_vessel_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_cities", []))
    await callback.message.edit_text("Location and Sailing Area:", reply_markup=get_cities_select_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))
    await state.set_state(Registration.vessel_location)
    await callback.answer()


@router.callback_query(Registration.vessel_type, F.data.startswith("vessel_type:"))
async def toggle_vessel_type(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_vessel_types", []))
    target_item = find_item_by_hash(VESSEL_TYPES, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_vessel_types=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back"))
    await callback.answer()


@router.callback_query(Registration.vessel_type, F.data == "vessel_type_done")
async def finish_vessel_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_vessel_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    await callback.message.edit_text(
        "Usage Format:",
        reply_markup=get_single_select_keyboard(VESSEL_USAGE_FORMAT, "vessel_usage", "vessel_usage_back")
    )
    await state.set_state(Registration.vessel_usage)
    await callback.answer()

@router.callback_query(Registration.vessel_usage, F.data == "vessel_usage_back")
async def back_from_vessel_usage(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_types", []))
    await callback.message.edit_text(
        "Type of Vessel\n\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back")
    )
    await state.set_state(Registration.vessel_type)
    await callback.answer()


@router.callback_query(Registration.vessel_usage, F.data.startswith("vessel_usage:"))
async def select_vessel_usage(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(VESSEL_USAGE_FORMAT, item_hash)
    if target_item:
        await state.update_data(vessel_usage=target_item)
    data = await state.get_data()
    selected = set(data.get("selected_vessel_safety", []))
    await callback.message.edit_text(
        "Safety and Documents:",
        reply_markup=get_multiselect_keyboard(VESSEL_SAFETY, selected, "vessel_safe", "vessel_safe_done", "vessel_safe_back")
    )
    await state.set_state(Registration.vessel_safety)
    await callback.answer()

@router.callback_query(Registration.vessel_safety, F.data == "vessel_safe_back")
async def back_from_vessel_safety(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Usage Format:",
        reply_markup=get_single_select_keyboard(VESSEL_USAGE_FORMAT, "vessel_usage", "vessel_usage_back")
    )
    await state.set_state(Registration.vessel_usage)
    await callback.answer()


@router.callback_query(Registration.vessel_safety, F.data.startswith("vessel_safe:"))
async def toggle_vessel_safety(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_vessel_safety", []))
    target_item = find_item_by_hash(VESSEL_SAFETY, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_vessel_safety=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(VESSEL_SAFETY, selected, "vessel_safe", "vessel_safe_done", "vessel_safe_back"))
    await callback.answer()


@router.callback_query(Registration.vessel_safety, F.data == "vessel_safe_done")
async def finish_vessel_safety(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_vessel_safety", []):
        await callback.answer("Please select at least one option.", show_alert=True)
        return

    data = await state.get_data()
    selected = set(data.get("selected_vessel_financial", []))
    await callback.message.edit_text(
        "Financial Terms:",
        reply_markup=get_multiselect_keyboard(VESSEL_FINANCIAL, selected, "vessel_fin", "vessel_fin_done", "vessel_fin_back")
    )
    await state.set_state(Registration.vessel_financial)
    await callback.answer()

@router.callback_query(Registration.vessel_financial, F.data == "vessel_fin_back")
async def back_from_vessel_fin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_safety", []))
    await callback.message.edit_text(
        "Safety and Documents:",
        reply_markup=get_multiselect_keyboard(VESSEL_SAFETY, selected, "vessel_safe", "vessel_safe_done", "vessel_safe_back")
    )
    await state.set_state(Registration.vessel_safety)
    await callback.answer()


@router.callback_query(Registration.vessel_financial, F.data.startswith("vessel_fin:"))
async def toggle_vessel_financial(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    selected = set(data.get("selected_vessel_financial", []))
    target_item = find_item_by_hash(VESSEL_FINANCIAL, item_hash)
    if target_item:
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_vessel_financial=list(selected))
        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(VESSEL_FINANCIAL, selected, "vessel_fin", "vessel_fin_done", "vessel_fin_back"))
    await callback.answer()


@router.callback_query(Registration.vessel_financial, F.data == "vessel_fin_done")
async def finish_vessel_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_vessel_financial", []):
        await callback.answer("Please select at least one option.", show_alert=True)
        return

    specialist_text = (
        "8|9 🩵 Specialists\n\n"
        "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "
        "brought clarity, or simply made life easier.\n\n"
        "Please list only those specialists you have personally worked with and can genuinely vouch for."
    )
    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
    await state.set_state(Registration.specialist_section)
    await callback.answer()

@router.callback_query(Registration.specialist_section, F.data == "spec_sec_back")
async def back_from_spec_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_financial", []))
    await callback.message.edit_text(
        "Financial Terms:",
        reply_markup=get_multiselect_keyboard(VESSEL_FINANCIAL, selected, "vessel_fin", "vessel_fin_done", "vessel_fin_back")
    )
    await state.set_state(Registration.vessel_financial)
    await callback.answer()


# --- Specialists Section ---

@router.callback_query(Registration.specialist_section, F.data == "specialist_skip")
async def skip_specialist_section(callback: CallbackQuery, state: FSMContext):
    artwork_text = (
        "9|9 🩵 Artworks\n\n"
        "If you're an artist, photographer, or creator — and your work carries meaning and intention — "
        "this is a space to share it with the community.\n\n"
        "By offering your work to fellow residents, you let it find a home where it will be genuinely seen and appreciated."
    )
    await callback.message.edit_text(artwork_text, reply_markup=get_section_intro_keyboard("artwork_start", "artwork_skip", "art_sec_back"))
    await state.set_state(Registration.artwork_section)
    await callback.answer()


@router.callback_query(Registration.specialist_section, F.data == "specialist_start")
async def start_specialist_section(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Select the category of specialists you can recommend:",
        reply_markup=get_category_keyboard(SPECIALIST_CATEGORIES, "spec_cat", "spec_cat_back")
    )
    await state.set_state(Registration.specialist_category)
    await callback.answer()

@router.callback_query(Registration.specialist_category, F.data == "spec_cat_back")
async def back_from_spec_cat(callback: CallbackQuery, state: FSMContext):
    specialist_text = (
        "8|9 🩵 Specialists\n\n"
        "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "
        "brought clarity, or simply made life easier.\n\n"
        "Please list only those specialists you have personally worked with and can genuinely vouch for."
    )
    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
    await state.set_state(Registration.specialist_section)
    await callback.answer()


@router.callback_query(Registration.specialist_category, F.data.startswith("spec_cat:"))
async def process_specialist_category(callback: CallbackQuery, state: FSMContext):
    category_key = callback.data.split(":")[1]
    await state.update_data(current_specialist_category=category_key)
    data = await state.get_data()
    selected = set(data.get("selected_specialist_items", []))
    category_name = SPECIALIST_CATEGORIES[category_key]["name"]
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the specialists you can recommend:",
        reply_markup=get_category_items_keyboard(category_key, SPECIALIST_CATEGORIES, selected, "spec_item", "spec_item_done", "spec_item_back")
    )
    await state.set_state(Registration.specialist_items)
    await callback.answer()

@router.callback_query(Registration.specialist_items, F.data == "spec_item_back")
async def back_from_spec_items(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Select the category of specialists you can recommend:",
        reply_markup=get_category_keyboard(SPECIALIST_CATEGORIES, "spec_cat", "spec_cat_back")
    )
    await state.set_state(Registration.specialist_category)
    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data.startswith("spec_item:"))
async def toggle_specialist_item(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    category_key = data.get("current_specialist_category")
    items_list = SPECIALIST_CATEGORIES.get(category_key, {}).get("items", [])
    target_item = find_item_by_hash(items_list, item_hash)
    if target_item:
        selected = set(data.get("selected_specialist_items", []))
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_specialist_items=list(selected))
        await callback.message.edit_reply_markup(
            reply_markup=get_category_items_keyboard(category_key, SPECIALIST_CATEGORIES, selected, "spec_item", "spec_item_done", "spec_item_back")
        )
    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data == "spec_back_cat")
async def back_to_specialist_categories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Select the category of specialists you can recommend:", reply_markup=get_category_keyboard(SPECIALIST_CATEGORIES, "spec_cat"))
    await state.set_state(Registration.specialist_category)
    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data == "spec_item_done")
async def finish_specialist_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_specialist_items", []):
         await callback.answer("Please select at least one item.", show_alert=True)
         return

    await callback.message.delete()
    await callback.message.answer(
        "Type of Connection:",
        reply_markup=get_single_select_keyboard(SPECIALIST_CONNECTION_TYPE, "spec_conn", "spec_conn_back")
    )
    await state.set_state(Registration.specialist_connection)
    await callback.answer()

@router.callback_query(Registration.specialist_connection, F.data == "spec_conn_back")
async def back_from_spec_conn(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_key = data.get("current_specialist_category")
    selected = set(data.get("selected_specialist_items", []))

    # We need to restore inline keyboard, so we edit_text if possible, but previous was deleted.
    # So we send new message.
    await callback.message.delete()
    await callback.message.answer(
        f"Category selected. Select specialists:",
        reply_markup=get_category_items_keyboard(category_key, SPECIALIST_CATEGORIES, selected, "spec_item", "spec_item_done", "spec_item_back")
    )
    await state.set_state(Registration.specialist_items)
    await callback.answer()


@router.callback_query(Registration.specialist_connection, F.data.startswith("spec_conn:"))
async def select_specialist_connection(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(SPECIALIST_CONNECTION_TYPE, item_hash)
    if target_item:
        await state.update_data(specialist_connection=target_item)

    await callback.message.delete()
    await callback.message.answer("Specialist Name\n\nPlease type the full name or public working name:", reply_markup=get_cancel_keyboard())
    await state.set_state(Registration.specialist_name)
    await callback.answer()


@router.message(Registration.specialist_name, F.text)
async def process_specialist_name(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await message.answer("Type of Connection:", reply_markup=get_single_select_keyboard(SPECIALIST_CONNECTION_TYPE, "spec_conn", "spec_conn_back"))
        await state.set_state(Registration.specialist_connection)
        return

    await state.update_data(specialist_name=message.text)
    await message.answer("Contact\n\nSpecify one or more (Telegram | WhatsApp | Email | Website | Social media):", reply_markup=get_cancel_keyboard())
    await state.set_state(Registration.specialist_contact)


@router.message(Registration.specialist_contact, F.text)
async def process_specialist_contact(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await message.answer("Specialist Name\n\nPlease type the full name or public working name:", reply_markup=get_cancel_keyboard())
        await state.set_state(Registration.specialist_name)
        return

    await state.update_data(specialist_contact=message.text)
    await message.answer(
        "Referral Phrase for Special Conditions\n\n"
        "Phrase the person should mention to confirm recommendation, e.g.:\n"
        "• \"From Anna, 10% off\"\n"
        "• \"Recommended by Anna\"\n"
        "• \"Joyseekers referral\"\n\n"
        "Type the phrase or '-' to skip:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.specialist_referral)


@router.message(Registration.specialist_referral, F.text)
async def process_specialist_referral(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await message.answer("Contact\n\nSpecify one or more (Telegram | WhatsApp | Email | Website | Social media):", reply_markup=get_cancel_keyboard())
        await state.set_state(Registration.specialist_contact)
        return

    referral = message.text if message.text != "-" else ""
    await state.update_data(specialist_referral=referral)

    # Save current specialist to list
    data = await state.get_data()
    new_spec = {
        "category": data.get("current_specialist_category"),
        "items": data.get("selected_specialist_items"),
        "connection": data.get("specialist_connection"),
        "name": data.get("specialist_name"),
        "contact": data.get("specialist_contact"),
        "referral": referral
    }
    specialists_list = data.get("specialists_list", [])
    specialists_list.append(new_spec)
    await state.update_data(specialists_list=specialists_list, selected_specialist_items=[])

    # Ask if user wants to add another specialist
    await message.answer(
        "Do you want to add another specialist?\n\nShare contacts of 3 people and get 1 free point for community exchanges 🩵",
        reply_markup=get_confirmation_keyboard("add_spec")
    )
    await state.set_state(Registration.specialist_loop_confirm)

@router.callback_query(Registration.specialist_loop_confirm, F.data.startswith("confirm:add_spec:"))
async def add_another_specialist(callback: CallbackQuery, state: FSMContext):
    # Loop back to category
    await callback.message.edit_text(
        "Select the category of specialists you can recommend:",
        reply_markup=get_category_keyboard(SPECIALIST_CATEGORIES, "spec_cat", "spec_cat_back")
    )
    await state.set_state(Registration.specialist_category)
    await callback.answer()

@router.callback_query(Registration.specialist_loop_confirm, F.data.startswith("cancel:add_spec"))
async def finish_specialist_loop(callback: CallbackQuery, state: FSMContext):
    # Move to Artworks section
    artwork_text = (
        "9|9 🩵 Artworks\n\n"
        "If you're an artist, photographer, or creator — and your work carries meaning and intention — "
        "this is a space to share it with the community.\n\n"
        "By offering your work to fellow residents, you let it find a home where it will be genuinely seen and appreciated."
    )
    await callback.message.edit_text(artwork_text, reply_markup=get_section_intro_keyboard("artwork_start", "artwork_skip", "art_sec_back"))
    await state.set_state(Registration.artwork_section)
    await callback.answer()

@router.callback_query(Registration.artwork_section, F.data == "art_sec_back")
async def back_from_art_section(callback: CallbackQuery, state: FSMContext):
    # Go back to specialist loop confirm? Or specialist start?
    # Logic: if list is not empty, go to confirm. Else go to start.
    data = await state.get_data()
    if data.get("specialists_list"):
         await callback.message.edit_text(
            "Do you want to add another specialist?\n\nShare contacts of 3 people and get 1 free point for community exchanges 🩵",
            reply_markup=get_confirmation_keyboard("add_spec")
        )
         await state.set_state(Registration.specialist_loop_confirm)
    else:
        specialist_text = (
            "8|9 🩵 Specialists\n\n"
            "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "
            "brought clarity, or simply made life easier.\n\n"
            "Please list only those specialists you have personally worked with and can genuinely vouch for."
        )
        await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
        await state.set_state(Registration.specialist_section)
    await callback.answer()


# --- Artworks Section ---

@router.callback_query(Registration.artwork_section, F.data == "artwork_skip")
async def skip_artwork_section(callback: CallbackQuery, state: FSMContext, db: Database):
    # Finalize registration
    await finish_registration(callback.message, state, db)
    await callback.answer()


@router.callback_query(Registration.artwork_section, F.data == "artwork_start")
async def start_artwork_section(callback: CallbackQuery, state: FSMContext):
    # Select Art Form
    await callback.message.edit_text(
        "Form of Art\n\nSelect:",
        reply_markup=get_single_select_keyboard(ART_FORMS, "art_form", "art_form_back")
    )
    await state.set_state(Registration.art_form)
    await callback.answer()

@router.callback_query(Registration.art_form, F.data == "art_form_back")
async def back_from_art_form(callback: CallbackQuery, state: FSMContext):
    artwork_text = (
        "9|9 🩵 Artworks\n\n"
        "If you're an artist, photographer, or creator — and your work carries meaning and intention — "
        "this is a space to share it with the community.\n\n"
        "By offering your work to fellow residents, you let it find a home where it will be genuinely seen and appreciated."
    )
    await callback.message.edit_text(artwork_text, reply_markup=get_section_intro_keyboard("artwork_start", "artwork_skip", "art_sec_back"))
    await state.set_state(Registration.artwork_section)
    await callback.answer()


@router.callback_query(Registration.art_form, F.data.startswith("art_form:"))
async def select_art_form(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(ART_FORMS, item_hash)
    if target_item:
        await state.update_data(art_form=target_item)

    await callback.message.edit_text(
        "Who is the author?",
        reply_markup=get_single_select_keyboard(ART_AUTHOR_TYPE, "art_auth", "art_auth_back")
    )
    await state.set_state(Registration.art_author)
    await callback.answer()

@router.callback_query(Registration.art_author, F.data == "art_auth_back")
async def back_from_art_author(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Form of Art\n\nSelect:",
        reply_markup=get_single_select_keyboard(ART_FORMS, "art_form", "art_form_back")
    )
    await state.set_state(Registration.art_form)
    await callback.answer()


@router.callback_query(Registration.art_author, F.data.startswith("art_auth:"))
async def select_art_author(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(ART_AUTHOR_TYPE, item_hash)
    if target_item:
        await state.update_data(art_author=target_item)

    await callback.message.delete()
    await callback.message.answer(
        "Author Name (or Pseudonym):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.art_author_name)
    await callback.answer()


@router.message(Registration.art_author_name, F.text)
async def process_art_author_name(message: Message, state: FSMContext):
    if message.text == "🔙 Back":
        await message.answer(
            "Who is the author?",
            reply_markup=get_single_select_keyboard(ART_AUTHOR_TYPE, "art_auth", "art_auth_back")
        )
        await state.set_state(Registration.art_author)
        return

    await state.update_data(art_author_name=message.text)

    # Remove previous keyboard if any (though get_cancel_keyboard is Reply)
    await message.answer("Processing...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Location of the Artwork:",
        reply_markup=get_cities_select_keyboard("art_city", "art_city_done", None, "art_city_back")
    )
    await state.set_state(Registration.art_location)

@router.callback_query(Registration.art_location, F.data == "art_city_back")
async def back_from_art_city(callback: CallbackQuery, state: FSMContext):
    # Back to text input
    await callback.message.delete()
    await callback.message.answer(
        "Author Name (or Pseudonym):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.art_author_name)
    await callback.answer()


@router.callback_query(Registration.art_location, F.data.startswith("art_city:"))
async def select_art_city(callback: CallbackQuery, state: FSMContext):
    city_hash = callback.data.split(":")[1]
    city = find_item_by_hash(CITIES, city_hash)
    if city:
        await state.update_data(art_location=city)
    # Single select for art city? Or multi? Prompt said "Location" singular.
    # Usually artwork is in one place.
    # But `get_cities_select_keyboard` is multi-select capable.
    # I'll treat it as single select if user clicks one, but the keyboard is built for multi.
    # Let's assume single select is enough for Art Location based on typical logic.
    # Update: prompt didn't specify multi for art.
    await callback.answer(f"Selected: {city}" if city else "")


@router.callback_query(Registration.art_location, F.data == "art_city_done")
async def finish_art_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Check if we need photo
    await callback.message.edit_text("Please upload a photo of the artwork (send as photo):")
    await state.set_state(Registration.art_photo)
    await callback.answer()

@router.message(Registration.art_photo, F.photo)
async def process_art_photo(message: Message, state: FSMContext, db: Database):
    # Save photo file_id
    photo_id = message.photo[-1].file_id
    await state.update_data(art_photo_id=photo_id)
    await finish_registration(message, state, db)

async def finish_registration(message: Message, state: FSMContext, db: Database):
    data = await state.get_data()

    user_id = message.from_user.id
    name = data.get("name", "Unknown")
    main_city = data.get("main_city", "Unknown")
    # current_city is removed, use main_city or default
    current_city = main_city
    about = data.get("about", "-")
    instagram = data.get("instagram", "-")
    username = message.from_user.username

    # Save user to DB
    await db.add_user(
        user_id=user_id,
        username=username,
        name=name,
        main_city=main_city,
        current_city=current_city,
        about=about,
        instagram=instagram
    )

    # Save answers (simple dump for now as per schema)
    await db.add_user_answer(user_id, "registration_data", json.dumps(data, default=str))

    summary = (
        f"Registration completed!\n\n"
        f"﹡Name - {name}\n"
        f"﹡City - {main_city}\n"
        f"﹡About - {about}\n"
        f"﹡Instagram - {instagram}\n"
        f"Points: 0"
    )

    await message.answer(summary, reply_markup=get_main_menu_keyboard())
    await state.clear()
