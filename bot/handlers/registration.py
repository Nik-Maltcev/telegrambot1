from aiogram import Router, F
from aiogram.types import InputMediaPhoto
from aiogram.types.input_file import FSInputFile



from aiogram.filters import CommandStart, Command



from aiogram.fsm.context import FSMContext



from aiogram.fsm.state import State, StatesGroup



from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User



from bot.database import Database



from bot.keyboards import (



    get_main_menu_keyboard, get_admin_menu_keyboard, get_cancel_keyboard,



    get_skill_categories_keyboard, get_skill_items_keyboard, get_multiselect_keyboard,



    get_paginated_multiselect_keyboard,



    get_single_select_keyboard, get_skip_keyboard, get_section_intro_keyboard,



    get_cities_select_keyboard, get_category_keyboard, get_category_items_keyboard,



    get_category_single_select_keyboard,



    get_confirmation_keyboard, get_vessel_locations_keyboard



)



from bot.config import ADMIN_IDS



from bot.form_data import (

 RESOURCE_ACCESS_CATEGORIES,
 SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS, RESULT_TYPES,

 CITIES, INTRO_CATEGORIES, 

 PROPERTY_TYPES, 

 VEHICLE_TYPES,

 EQUIPMENT_TYPES, 

 AIRCRAFT_TYPES, 

 VESSEL_TYPES, VESSEL_LOCATIONS,

 SPECIALIST_CATEGORIES, SPECIALIST_CONNECTION_TYPE,

 ART_FORMS)



import json



import hashlib

import pathlib



import asyncio





router = Router()

RESOURCE_ACCESS_CATEGORY_ORDER = list(RESOURCE_ACCESS_CATEGORIES.keys())


def _get_next_ra_category(category_key: str):
    if category_key not in RESOURCE_ACCESS_CATEGORY_ORDER:
        return None
    idx = RESOURCE_ACCESS_CATEGORY_ORDER.index(category_key)
    if idx + 1 < len(RESOURCE_ACCESS_CATEGORY_ORDER):
        return RESOURCE_ACCESS_CATEGORY_ORDER[idx + 1]
    return None


async def _show_ra_category_items(callback: CallbackQuery, state: FSMContext, category_key: str):
    data = await state.get_data()
    selected = set(data.get("selected_ra_items", []))
    category_name = RESOURCE_ACCESS_CATEGORIES[category_key]["name"]
    next_category_key = _get_next_ra_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    await state.update_data(ra_item_page=0)
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the resources you own or manage:\nYou can select multiple",
        reply_markup=get_category_items_keyboard(
            category_key,
            RESOURCE_ACCESS_CATEGORIES,
            selected,
            "ra_item",
            "ra_item_done",
            "ra_back_cat",
            page=0,
            page_callback_prefix="ra_item_page",
            done_text=done_text,
        )
    )


SKILL_CATEGORY_ORDER = list(SKILL_CATEGORIES.keys())


def _get_next_skill_category(category_key: str):
    if category_key not in SKILL_CATEGORY_ORDER:
        return None
    idx = SKILL_CATEGORY_ORDER.index(category_key)
    if idx + 1 < len(SKILL_CATEGORY_ORDER):
        return SKILL_CATEGORY_ORDER[idx + 1]
    return None


async def _show_skill_category_items(callback: CallbackQuery, state: FSMContext, category_key: str):
    data = await state.get_data()
    selected = set(data.get("selected_skill_items", []))
    category_name = SKILL_CATEGORIES[category_key]["name"]
    next_category_key = _get_next_skill_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    await state.update_data(q_item_page=0)
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect specific skills, services, or areas:\nYou can select multiple",
        reply_markup=get_category_items_keyboard(
            category_key,
            SKILL_CATEGORIES,
            selected,
            "q_item",
            "q_item_done",
            "skill_back_cat",
            page=0,
            page_callback_prefix="q_item_page",
            done_text=done_text,
        )
    )



INTRO_CATEGORY_ORDER = list(INTRO_CATEGORIES.keys())

SPEC_CATEGORY_ORDER = list(SPECIALIST_CATEGORIES.keys())


def _get_next_intro_category(category_key: str):
    if category_key not in INTRO_CATEGORY_ORDER:
        return None
    idx = INTRO_CATEGORY_ORDER.index(category_key)
    if idx + 1 < len(INTRO_CATEGORY_ORDER):
        return INTRO_CATEGORY_ORDER[idx + 1]
    return None


async def _show_intro_category_items(callback: CallbackQuery, state: FSMContext, category_key: str):
    data = await state.get_data()
    selected = set(data.get("selected_intro_items", []))
    category_name = INTRO_CATEGORIES[category_key]["name"]
    next_category_key = _get_next_intro_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    if category_key == "private_events":
        prompt_text = (
            f"Category: {category_name}\n\n"
            "This section is about events and gatherings that don't usually show up "
            "in public listings, where access comes through connections rather than tickets.\n\n"
            "Select events you can provide access to for other residents:"
        )
    else:
        prompt_text = f"Category: {category_name}\n\nSelect the people you can introduce:"

    await state.update_data(intro_item_page=0)
    await callback.message.edit_text(
        prompt_text,
        reply_markup=get_category_items_keyboard(
            category_key,
            INTRO_CATEGORIES,
            selected,
            "intro_item",
            "intro_item_done",
            "intro_back_cat",
            page=0,
            page_callback_prefix="intro_item_page",
            done_text=done_text,
        )
    )


def _get_next_spec_category(category_key: str):
    if category_key not in SPEC_CATEGORY_ORDER:
        return None
    idx = SPEC_CATEGORY_ORDER.index(category_key)
    if idx + 1 < len(SPEC_CATEGORY_ORDER):
        return SPEC_CATEGORY_ORDER[idx + 1]
    return None


async def _show_spec_category_items(callback: CallbackQuery, state: FSMContext, category_key: str):
    data = await state.get_data()
    selected = set(data.get("selected_specialist_items", []))
    category_name = SPECIALIST_CATEGORIES[category_key]["name"]
    next_category_key = _get_next_spec_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    await state.update_data(spec_item_page=0)
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the specialists you can recommend:",
        reply_markup=get_category_items_keyboard(
            category_key,
            SPECIALIST_CATEGORIES,
            selected,
            "spec_item",
            "spec_item_done",
            "spec_back_cat",
            page=0,
            page_callback_prefix="spec_item_page",
            done_text=done_text,
        )
    )






def find_item_by_hash(items_list, item_hash):



    """Helper to find item by its hash"""



    for item in items_list:



        if hashlib.md5(item.encode()).hexdigest()[:8] == item_hash:



            return item



    return None


async def _redraw_multiselect_page(
    callback: CallbackQuery,
    state: FSMContext,
    *,
    page_key: str,
    selected_key: str,
    options: list,
    prefix: str,
    done_callback: str,
    back_callback: str,
):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    selected = set(data.get(selected_key, []))
    await state.update_data(**{page_key: page})
    await callback.message.edit_reply_markup(
        reply_markup=get_multiselect_keyboard(
            options,
            selected,
            prefix,
            done_callback,
            back_callback,
            page=page,
            page_callback_prefix=page_key,
        )
    )
    await callback.answer()


async def _redraw_category_items_page(
    callback: CallbackQuery,
    state: FSMContext,
    *,
    page_key: str,
    selected_key: str,
    current_category_key: str,
    categories: dict,
    prefix: str,
    done_callback: str,
    back_callback: str,
):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    selected = set(data.get(selected_key, []))
    category_key = data.get(current_category_key)
    if not category_key:
        await callback.answer()
        return
    await state.update_data(**{page_key: page})
    await callback.message.edit_reply_markup(
        reply_markup=get_category_items_keyboard(
            category_key,
            categories,
            selected,
            prefix,
            done_callback,
            back_callback,
            page=page,
            page_callback_prefix=page_key,
        )
    )
    await callback.answer()





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

    # Resources & Access section
    resource_access_section = State()
    resource_access_items = State()
    resource_access_location = State()

    # Skills section



    skill_category = State() # Deprecated but keeping index safe



    skill_items = State()



    offer_formats = State()

    result_type = State()





    # Personal Introductions section



    intro_section = State()



    intro_category = State()



    intro_items = State()



    intro_location = State()





    # Real Estate section



    real_estate_section = State()



    property_location = State() # Moved first



    property_type = State()





    # Cars section



    cars_section = State()



    car_location = State() # Moved first



    car_info = State()





    # Equipment section



    equipment_section = State()



    equipment_location = State() # Moved first



    equipment_types = State()





    # Air Transport section



    aircraft_section = State()



    aircraft_location = State() # Moved first



    aircraft_type = State()





    # Water Transport section



    vessel_section = State()



    vessel_location = State() # Moved first



    vessel_type = State()





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



    art_author_name = State()



    art_location = State()



    art_link = State() # Link to artwork





    # Maps section (share Google Maps)



    maps_section = State()



    maps_city = State()



    maps_link = State()



    maps_add_more = State()





    # Initial step



    waiting_for_invite_code = State()





@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(Registration.skill_items, F.data.startswith("q_item_page:"))
async def page_skill_items(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    category_key = data.get("current_skill_category")
    if not category_key:
        await callback.answer()
        return

    await state.update_data(q_item_page=page)
    selected = set(data.get("selected_skill_items", []))
    next_category_key = _get_next_skill_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    await callback.message.edit_reply_markup(
        reply_markup=get_category_items_keyboard(
            category_key,
            SKILL_CATEGORIES,
            selected,
            "q_item",
            "q_item_done",
            "skill_back_cat",
            page=page,
            page_callback_prefix="q_item_page",
            done_text=done_text,
        )
    )
    await callback.answer()


@router.callback_query(Registration.offer_formats, F.data.startswith("q_fmt_page:"))
async def page_offer_formats(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="q_fmt_page",
        selected_key="selected_offer_formats",
        options=OFFER_FORMATS,
        prefix="q_fmt",
        done_callback="q_fmt_done",
        back_callback="q_fmt_back",
    )


@router.callback_query(Registration.result_type, F.data.startswith("q_res_page:"))
async def page_result_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="q_res_page",
        selected_key="selected_result_types",
        options=RESULT_TYPES,
        prefix="q_res",
        done_callback="q_res_done",
        back_callback="q_res_back",
    )


@router.callback_query(Registration.intro_items, F.data.startswith("intro_item_page:"))
async def page_intro_items(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    category_key = data.get("current_intro_category")
    if not category_key:
        await callback.answer()
        return

    await state.update_data(intro_item_page=page)
    selected = set(data.get("selected_intro_items", []))
    next_category_key = _get_next_intro_category(category_key)
    done_text = "Next ➡️" if next_category_key else "🆗 Done"

    await callback.message.edit_reply_markup(
        reply_markup=get_category_items_keyboard(
            category_key,
            INTRO_CATEGORIES,
            selected,
            "intro_item",
            "intro_item_done",
            "intro_back_cat",
            page=page,
            page_callback_prefix="intro_item_page",
            done_text=done_text,
        )
    )
    await callback.answer()


@router.callback_query(Registration.property_type, F.data.startswith("prop_type_page:"))
async def page_property_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="prop_type_page",
        selected_key="selected_property_types",
        options=PROPERTY_TYPES,
        prefix="prop_type",
        done_callback="prop_type_done",
        back_callback="prop_type_back",
    )


@router.callback_query(Registration.car_info, F.data.startswith("car_type_page:"))
async def page_car_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="car_type_page",
        selected_key="selected_vehicle_types",
        options=VEHICLE_TYPES,
        prefix="car_type",
        done_callback="car_type_done",
        back_callback="car_type_back",
    )


@router.callback_query(Registration.equipment_types, F.data.startswith("equip_type_page:"))
async def page_equipment_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="equip_type_page",
        selected_key="selected_equipment_types",
        options=EQUIPMENT_TYPES,
        prefix="equip_type",
        done_callback="equip_type_done",
        back_callback="equip_type_back",
    )


@router.callback_query(Registration.aircraft_type, F.data.startswith("air_type_page:"))
async def page_aircraft_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="air_type_page",
        selected_key="selected_aircraft_types",
        options=AIRCRAFT_TYPES,
        prefix="air_type",
        done_callback="air_type_done",
        back_callback="air_type_back",
    )


@router.callback_query(Registration.vessel_type, F.data.startswith("vessel_type_page:"))
async def page_vessel_type(callback: CallbackQuery, state: FSMContext):
    await _redraw_multiselect_page(
        callback,
        state,
        page_key="vessel_type_page",
        selected_key="selected_vessel_types",
        options=VESSEL_TYPES,
        prefix="vessel_type",
        done_callback="vessel_type_done",
        back_callback="vessel_type_back",
    )


@router.message(Registration.waiting_for_invite_code, F.text)



async def process_initial_invite_code(message: Message, state: FSMContext):



    invite_code = message.text.strip()



    if invite_code.upper() == "JOY":



        await state.update_data(



            selected_ra_items=[],
            selected_skill_items=[], selected_offer_formats=[],



            selected_intro_items=[],



            selected_property_types=[], selected_equipment_types=[],



            selected_specialist_items=[], selected_art_forms=[],



            # Multi-select cities initialization



            selected_prop_cities=[], selected_car_cities=[],



            selected_equip_cities=[], selected_air_cities=[],



            selected_vessel_cities=[], selected_intro_cities=[],



            # Specialists list initialization



            specialists_list=[],



            # Vehicle types multi-select



            selected_vehicle_types=[],



            # Aircraft types multi-select



            selected_aircraft_types=[],



            # Vessel types multi-select



            selected_vessel_types=[]



        )





        # Send welcome images as media group

        images_dir = pathlib.Path(__file__).parent.parent / "images"

        media = [

            InputMediaPhoto(media=FSInputFile(images_dir / "1.JPG")),

            InputMediaPhoto(media=FSInputFile(images_dir / "2.JPG")),

            InputMediaPhoto(media=FSInputFile(images_dir / "3.JPG")),

            InputMediaPhoto(media=FSInputFile(images_dir / "4.JPG")),

            InputMediaPhoto(media=FSInputFile(images_dir / "5.JPG")),

            InputMediaPhoto(media=FSInputFile(images_dir / "6.JPG")),

        ]

        await message.answer("Read this, luv.")
        await message.answer_media_group(media)



        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])

        await message.answer("👇🏻 Click below to continue:", reply_markup=keyboard)



    else:



        await message.answer("❌ Invalid invite code. Please try again.")





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



        await message.answer("Please enter the invite code:", reply_markup=ReplyKeyboardRemove())



        await state.set_state(Registration.waiting_for_invite_code)





@router.callback_query(F.data == "intro_sounds_good")



async def process_intro_sounds_good(callback: CallbackQuery, state: FSMContext):



    warning_text = (



        "complete the questionnaire carefully and you'll receive 1 point to exchange within the community 💙\n"



        "10 sections, ~10 minutes.\n\n"



        "incomplete submissions are not reviewed and will not be granted access to the Community.\n\n"



        "the bot will send questions one by one — just reply in chat or choose the available options.\n\n"



        "you can update or change your information at any time by contacting our manager via direct messages @papacaralya"



    )



    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="OK", callback_data="warning_ok")]])



    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(warning_text, reply_markup=keyboard)



    await callback.answer()





@router.callback_query(F.data == "warning_ok")



async def process_warning_ok(callback: CallbackQuery, state: FSMContext):



    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("Please enter your name:", reply_markup=get_cancel_keyboard())



    await state.set_state(Registration.name)



    await callback.answer()





@router.message(Registration.name, F.text)



async def process_name(message: Message, state: FSMContext):



    if message.text.strip() == "🔙 Back":



        # Back to Intro



        intro_text = (



            "hi luv! and welcome to joyseekers 🩵\n\n"



            "you’re now part of a closed community of people who travel, do what they love, grow — and support each other through shared resources and opportunities.\n\n"



            "inside joyseekers you can connect worldwide, exchange skills, receive trusted introductions, explore real estate, and access shared assets like cars or equipment.\n\n"



            "the system is simple:\n"



            "1 shared resource = 1 credit, which you can use to unlock something in return.\n\n"



            "to get started, just fill out a short questionnaire and add what you’re open to sharing.\n"



            "after a quick approval by me, all sections will be unlocked.\n\n"



            "not everyone finds this space — and that’s what makes it special.\n"



            "glad to be here with you.\n"



            "stay joyful 🩵\n"



            "xx Anna"



        )



        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])



        await message.answer(intro_text, reply_markup=keyboard)



        await state.clear()



        return



    await state.update_data(name=message.text)





    # Initialize empty selection for main city



    await state.update_data(selected_main_cities=[])





    city_msg = await message.answer(
        "Great! Now, please select the city (or cities) where you are usually located:",
        reply_markup=get_cities_select_keyboard("main_city", "main_city_done", set(), "main_city_back"),
    )
    await state.update_data(city_prompt_message_id=city_msg.message_id)



    await state.set_state(Registration.main_city)





@router.message(Registration.main_city, F.text)



async def process_main_city_text(message: Message, state: FSMContext):



    # This handler might catch text if user types instead of clicking



    # If it is "Back", we go back.



    if message.text.strip() == "🔙 Back":



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





    try:
        await callback.message.delete() # Remove inline keyboard with city selection
    except Exception:
        pass



    await callback.message.answer("Please enter your Instagram username (or send '-' if you don't have one):", reply_markup=get_cancel_keyboard())



    await state.set_state(Registration.instagram)



    await callback.answer()





@router.message(Registration.instagram, F.text)



async def process_instagram(message: Message, state: FSMContext):



    if message.text.strip() == "🔙 Back":



        await state.set_state(Registration.main_city)



        await message.answer("Select cities:", reply_markup=get_cities_select_keyboard("main_city", "main_city_done", set(), "main_city_back"))



        return



    instagram = message.text if message.text != "-" else ""



    await state.update_data(instagram=instagram)





    # Ask for About info



    await message.answer(



        "Tell us a bit about yourself\nDescribe it shortly — just a few words.\nIn one of the next questions, you'll be able to share more details.\n\nExamples:\nArtist · Community creator\nFounder · Creative entrepreneur\nDJ · Music curator",



        reply_markup=get_cancel_keyboard()



    )



    await state.set_state(Registration.about)





@router.message(Registration.about, F.text)



async def process_about(message: Message, state: FSMContext):



    if message.text.strip() == "🔙 Back":



        await state.set_state(Registration.instagram)



        await message.answer("Please enter your Instagram username (or send '-' if you don't have one):", reply_markup=get_cancel_keyboard())



        return



    



    await state.update_data(about=message.text)

    ra_intro = (
        "1|11 🏢 Businesses, Spaces & Platforms\n\n"
        "Please indicate the businesses, spaces, or platforms you own or manage "
        "that other residents could collaborate with or use.\n\n"
        "These resources help create opportunities for partnerships, projects, "
        "and shared growth within the community."
    )

    await message.answer(
        ra_intro,
        reply_markup=get_section_intro_keyboard("ra_start", "ra_skip", "ra_sec_back")
    )

    await state.set_state(Registration.resource_access_section)






# ============ Businesses, Spaces & Platforms Section ============

@router.callback_query(Registration.resource_access_section, F.data == "ra_sec_back")
async def back_from_ra_section(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Tell us a bit about yourself\nDescribe it shortly — just a few words.\n"
        "In one of the next questions, you'll be able to share more details.\n\n"
        "Examples:\nArtist · Community creator\nFounder · Creative entrepreneur\nDJ · Music curator",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.about)
    await callback.answer()


@router.callback_query(Registration.resource_access_section, F.data == "ra_skip")
async def skip_ra_section(callback: CallbackQuery, state: FSMContext):
    # Move to Skills section
    first_category_key = SKILL_CATEGORY_ORDER[0]
    first_category_name = SKILL_CATEGORIES[first_category_key]["name"]

    skills_intro = (
        "2|11 \U0001f9d1\U0001f3fc\u200d\U0001f4bb Skills and Knowledge\n\n"
        "Please provide information about the skills, knowledge, and professional abilities "
        "you are willing to share with the community.\n\n"
        "Each of us carries unique mastery. Here you can list the areas where you can:\n"
        "\u2022 give a thoughtful consultation\n"
        "\u2022 teach your skill or method\n"
        "\u2022 guide someone through a process\n"
        "\u2022 create or deliver a clear final result\n\n"
        f"Category: {first_category_name}\n\n"
        "Select specific skills, services, or areas:\n"
        "You can select multiple"
    )

    await callback.message.edit_text(
        skills_intro,
        reply_markup=get_category_items_keyboard(
            first_category_key,
            SKILL_CATEGORIES,
            set(),
            "q_item",
            "q_item_done",
            "skill_back_cat",
            page=0,
            page_callback_prefix="q_item_page",
            done_text="Next \u27a1\ufe0f",
        )
    )

    await state.update_data(current_skill_category=first_category_key, q_item_page=0)
    await state.set_state(Registration.skill_items)
    await callback.answer()


@router.callback_query(Registration.resource_access_section, F.data == "ra_start")
async def start_ra_section(callback: CallbackQuery, state: FSMContext):
    first_category = RESOURCE_ACCESS_CATEGORY_ORDER[0]
    await state.update_data(current_ra_category=first_category, ra_item_page=0)
    await _show_ra_category_items(callback, state, first_category)
    await state.set_state(Registration.resource_access_items)
    await callback.answer()


@router.callback_query(Registration.resource_access_items, F.data.startswith("ra_item:"))
async def toggle_ra_item(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    category_key = data.get("current_ra_category")
    items_list = RESOURCE_ACCESS_CATEGORIES.get(category_key, {}).get("items", [])
    target_item = find_item_by_hash(items_list, item_hash)
    if target_item:
        selected = set(data.get("selected_ra_items", []))
        if target_item in selected:
            selected.remove(target_item)
        else:
            selected.add(target_item)
        await state.update_data(selected_ra_items=list(selected))
        next_category_key = _get_next_ra_category(category_key)
        await callback.message.edit_reply_markup(
            reply_markup=get_category_items_keyboard(
                category_key,
                RESOURCE_ACCESS_CATEGORIES,
                selected,
                "ra_item",
                "ra_item_done",
                "ra_back_cat",
                page=data.get("ra_item_page", 0),
                page_callback_prefix="ra_item_page",
                done_text="Next \u27a1\ufe0f" if next_category_key else "\U0001f197 Done"
            )
        )
    await callback.answer()


@router.callback_query(Registration.resource_access_items, F.data.startswith("ra_item_page:"))
async def page_ra_items(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    category_key = data.get("current_ra_category")
    selected = set(data.get("selected_ra_items", []))
    await state.update_data(ra_item_page=page)
    next_category_key = _get_next_ra_category(category_key)
    await callback.message.edit_reply_markup(
        reply_markup=get_category_items_keyboard(
            category_key,
            RESOURCE_ACCESS_CATEGORIES,
            selected,
            "ra_item",
            "ra_item_done",
            "ra_back_cat",
            page=page,
            page_callback_prefix="ra_item_page",
            done_text="Next \u27a1\ufe0f" if next_category_key else "\U0001f197 Done"
        )
    )
    await callback.answer()


@router.callback_query(Registration.resource_access_items, F.data == "ra_back_cat")
async def back_from_ra_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_category = data.get("current_ra_category")
    if current_category in RESOURCE_ACCESS_CATEGORY_ORDER:
        idx = RESOURCE_ACCESS_CATEGORY_ORDER.index(current_category)
        if idx > 0:
            prev_category = RESOURCE_ACCESS_CATEGORY_ORDER[idx - 1]
            await state.update_data(current_ra_category=prev_category, ra_item_page=0)
            await _show_ra_category_items(callback, state, prev_category)
            await callback.answer()
            return
    # Back to section intro
    ra_intro = (
        "1|11 \U0001f3e2 Businesses, Spaces & Platforms\n\n"
        "Please indicate the businesses, spaces, or platforms you own or manage "
        "that other residents could collaborate with or use.\n\n"
        "These resources help create opportunities for partnerships, projects, "
        "and shared growth within the community."
    )
    await callback.message.edit_text(
        ra_intro,
        reply_markup=get_section_intro_keyboard("ra_start", "ra_skip", "ra_sec_back")
    )
    await state.set_state(Registration.resource_access_section)
    await callback.answer()


@router.callback_query(Registration.resource_access_items, F.data == "ra_item_done")
async def finish_ra_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_category = data.get("current_ra_category")
    next_category = _get_next_ra_category(current_category)

    if next_category:
        await state.update_data(current_ra_category=next_category, ra_item_page=0)
        await _show_ra_category_items(callback, state, next_category)
        await callback.answer()
        return

    # Move to Skills section
    first_category_key = SKILL_CATEGORY_ORDER[0]
    first_category_name = SKILL_CATEGORIES[first_category_key]["name"]

    skills_intro = (
        "2|11 \U0001f9d1\U0001f3fc\u200d\U0001f4bb Skills and Knowledge\n\n"
        "Please provide information about the skills, knowledge, and professional abilities "
        "you are willing to share with the community.\n\n"
        "Each of us carries unique mastery. Here you can list the areas where you can:\n"
        "\u2022 give a thoughtful consultation\n"
        "\u2022 teach your skill or method\n"
        "\u2022 guide someone through a process\n"
        "\u2022 create or deliver a clear final result\n\n"
        f"Category: {first_category_name}\n\n"
        "Select specific skills, services, or areas:\n"
        "You can select multiple"
    )

    await callback.message.edit_text(
        skills_intro,
        reply_markup=get_category_items_keyboard(
            first_category_key,
            SKILL_CATEGORIES,
            set(),
            "q_item",
            "q_item_done",
            "skill_back_cat",
            page=0,
            page_callback_prefix="q_item_page",
            done_text="Next \u27a1\ufe0f",
        )
    )

    await state.update_data(current_skill_category=first_category_key, q_item_page=0)
    await state.set_state(Registration.skill_items)
    await callback.answer()


@router.callback_query(Registration.skill_category, F.data == "skill_cat_back")



async def back_from_skill_category(callback: CallbackQuery, state: FSMContext):
    ra_intro = (
        "1|11 🏢 Businesses, Spaces & Platforms\n\n"
        "Please indicate the businesses, spaces, or platforms you own or manage "
        "that other residents could collaborate with or use.\n\n"
        "These resources help create opportunities for partnerships, projects, "
        "and shared growth within the community."
    )
    await callback.message.edit_text(
        ra_intro,
        reply_markup=get_section_intro_keyboard("ra_start", "ra_skip", "ra_sec_back")
    )
    await state.set_state(Registration.resource_access_section)
    await callback.answer()


@router.callback_query(Registration.skill_category, F.data.startswith("skill_cat:"))

async def process_skill_category_selection(callback: CallbackQuery, state: FSMContext):

    category_key = callback.data.split(":")[1]

    await state.update_data(current_skill_category=category_key, q_item_page=0)

    await _show_skill_category_items(callback, state, category_key)

    await state.set_state(Registration.skill_items)

    await callback.answer()



@router.callback_query(Registration.skill_items, F.data == "skill_back_cat")

async def back_to_skill_categories(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    current_category = data.get("current_skill_category")

    if current_category in SKILL_CATEGORY_ORDER:

        idx = SKILL_CATEGORY_ORDER.index(current_category)

        if idx > 0:

            prev_category = SKILL_CATEGORY_ORDER[idx - 1]

            await state.update_data(current_skill_category=prev_category, q_item_page=0)

            await _show_skill_category_items(callback, state, prev_category)

            await callback.answer()

            return

    await callback.message.delete()

    await callback.message.answer(

        "Tell us a bit about yourself\nDescribe it shortly — just a few words.\nIn one of the next questions, you'll be able to share more details.\n\nExamples:\nArtist · Community creator\nFounder · Creative entrepreneur\nDJ · Music curator",

        reply_markup=get_cancel_keyboard()

    )

    await state.set_state(Registration.about)

    await callback.answer()



@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))

async def process_skill_item_toggle(callback: CallbackQuery, state: FSMContext):

    item_hash = callback.data.split(":")[1]

    data = await state.get_data()

    category_key = data.get("current_skill_category")



    # Search in current category items

    items_list = SKILL_CATEGORIES.get(category_key, {}).get("items", [])

    target_item = find_item_by_hash(items_list, item_hash)



    if target_item:

        selected_items = set(data.get("selected_skill_items", []))

        if target_item in selected_items:

            selected_items.remove(target_item)

        else:

            selected_items.add(target_item)

        await state.update_data(selected_skill_items=list(selected_items))

        next_category_key = _get_next_skill_category(category_key)

        await callback.message.edit_reply_markup(

            reply_markup=get_category_items_keyboard(

                category_key,
                SKILL_CATEGORIES,
                selected_items,
                "q_item",
                "q_item_done",
                "skill_back_cat",
                page=data.get("q_item_page", 0),
                page_callback_prefix="q_item_page",
                done_text="Next ➡️" if next_category_key else "🆗 Done"

            )

        )

    await callback.answer()



@router.callback_query(Registration.skill_items, F.data == "q_item_done")

async def finish_skill_items(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    selected_items = data.get("selected_skill_items", [])

    current_category = data.get("current_skill_category")
    next_category = _get_next_skill_category(current_category)

    if next_category:
        await state.update_data(current_skill_category=next_category, q_item_page=0)
        await _show_skill_category_items(callback, state, next_category)
        await callback.answer()
        return

    if not selected_items:

        await callback.answer("Please select at least one skill.", show_alert=True)

        return

    if next_category:
        await state.update_data(current_skill_category=next_category, q_item_page=0)
        await _show_skill_category_items(callback, state, next_category)
        await callback.answer()
        return

    selected = set(data.get("selected_offer_formats", []))

    await callback.message.edit_text(

        "Formats You Offer\n\nSelect the formats in which you can share your expertise:\nYou can select multiple",

        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back", page=data.get("q_fmt_page", 0), page_callback_prefix="q_fmt_page")

    )

    await state.set_state(Registration.offer_formats)

    await callback.answer()



# Back from offer formats



@router.callback_query(Registration.offer_formats, F.data == "q_fmt_back")



async def back_from_offer_formats(callback: CallbackQuery, state: FSMContext):



    last_category = SKILL_CATEGORY_ORDER[-1]
    await state.update_data(current_skill_category=last_category, q_item_page=0)

    await _show_skill_category_items(callback, state, last_category)

    await state.set_state(Registration.skill_items)

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



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back", page=data.get("q_fmt_page", 0), page_callback_prefix="q_fmt_page"))



    await callback.answer()





@router.callback_query(Registration.offer_formats, F.data == "q_fmt_done")



async def finish_offer_formats(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected_items = data.get("selected_offer_formats", [])



    if not selected_items:



        await callback.answer("Please select at least one format.", show_alert=True)



        return





    # Move to Result Type selection
    selected = set(data.get("selected_result_types", []))
    await callback.message.edit_text(
        "Type of Result\n\nWhat kind of result can you provide?",
        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back", page=data.get("q_res_page", 0), page_callback_prefix="q_res_page")
    )
    await state.set_state(Registration.result_type)
    await callback.answer()





@router.callback_query(Registration.intro_section, F.data == "intro_sec_back")

async def back_to_result_type(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    selected = set(data.get("selected_result_types", []))

    await callback.message.edit_text(

        "Type of Result\n\nWhat kind of result can you provide?",

        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back", page=data.get("q_res_page", 0), page_callback_prefix="q_res_page")

    )

    await state.set_state(Registration.result_type)

    await callback.answer()







@router.callback_query(Registration.result_type, F.data == "q_res_back")

async def back_from_result_type(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    selected = set(data.get("selected_offer_formats", []))

    await callback.message.edit_text(

        "Formats You Offer\n\nSelect the formats in which you can share your expertise:\nYou can select multiple",

        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back", page=data.get("q_fmt_page", 0), page_callback_prefix="q_fmt_page")

    )

    await state.set_state(Registration.offer_formats)

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

        await callback.message.edit_reply_markup(

            reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back", page=data.get("q_res_page", 0), page_callback_prefix="q_res_page")

        )

    await callback.answer()





@router.callback_query(Registration.result_type, F.data == "q_res_done")

async def finish_result_type(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    if not data.get("selected_result_types", []):

        await callback.answer("Please select at least one option.", show_alert=True)

        return



    # Move to Personal Introductions section

    intro_text = (

        "3|11 🤝🏻 Personal Introduction\n\n"

        "In almost every life story, there is a moment when someone opened a door for us.\n\n"

        "Here, you can describe the key people in your orbit — founders, creators, innovators, "

        "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"

        "Titles are indicative. If your contact is a decision maker, list them in the closest category."

    )

    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))

    await state.set_state(Registration.intro_section)

    await callback.answer()

# --- Personal Introductions Section ---





@router.callback_query(Registration.intro_section, F.data == "intro_skip")



async def skip_intro_section(callback: CallbackQuery, state: FSMContext):



    # Move to Real Estate section



    real_estate_text = (



        "4|11 🗽 Real Estate\n\n"



        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "



        "to host another resident in a separate room — this is where you can share it with the community.\n\n"



        "Please list only the properties you are willing to share within a mutual exchange of community resources."



    )



    await callback.message.edit_text(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))



    await state.set_state(Registration.real_estate_section)



    await callback.answer()





@router.callback_query(Registration.intro_section, F.data == "intro_start")

async def start_intro_section(callback: CallbackQuery, state: FSMContext):

    first_category = INTRO_CATEGORY_ORDER[0]
    await state.update_data(current_intro_category=first_category, intro_item_page=0)

    await _show_intro_category_items(callback, state, first_category)

    await state.set_state(Registration.intro_items)

    await callback.answer()



@router.callback_query(Registration.intro_category, F.data == "intro_cat_back")



async def back_to_intro_section(callback: CallbackQuery, state: FSMContext):



    intro_text = (



        "3|11 🤝🏻 Personal Introduction\n\n"



        "In almost every life story, there is a moment when someone opened a door for us.\n\n"



        "Here, you can describe the key people in your orbit — founders, creators, innovators, "



        "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"



        "Titles are indicative. If your contact is a decision maker, list them in the closest category."



    )



    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))



    await state.set_state(Registration.intro_section)



    await callback.answer()





@router.callback_query(Registration.intro_category, F.data.startswith("intro_cat:"))

async def process_intro_category(callback: CallbackQuery, state: FSMContext):

    category_key = callback.data.split(":")[1]

    await state.update_data(current_intro_category=category_key, intro_item_page=0)

    await _show_intro_category_items(callback, state, category_key)

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

        next_category_key = _get_next_intro_category(category_key)

        await callback.message.edit_reply_markup(

            reply_markup=get_category_items_keyboard(
                category_key,
                INTRO_CATEGORIES,
                selected,
                "intro_item",
                "intro_item_done",
                "intro_back_cat",
                page=data.get("intro_item_page", 0),
                page_callback_prefix="intro_item_page",
                done_text="Next ➡️" if next_category_key else "🆗 Done"
            )

        )

    await callback.answer()



@router.callback_query(Registration.intro_items, F.data == "intro_back_cat")

async def back_to_intro_categories(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_category = data.get("current_intro_category")

    if current_category in INTRO_CATEGORY_ORDER:
        idx = INTRO_CATEGORY_ORDER.index(current_category)
        if idx > 0:
            prev_category = INTRO_CATEGORY_ORDER[idx - 1]
            await state.update_data(current_intro_category=prev_category, intro_item_page=0)
            await _show_intro_category_items(callback, state, prev_category)
            await callback.answer()
            return

    intro_text = (
        "3|11 🤝🏻 Personal Introduction\n\n"
        "In almost every life story, there is a moment when someone opened a door for us.\n\n"
        "Here, you can describe the key people in your orbit — founders, creators, innovators, "
        "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"
        "Titles are indicative. If your contact is a decision maker, list them in the closest category."
    )
    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))

    await state.set_state(Registration.intro_section)

    await callback.answer()



@router.callback_query(Registration.intro_items, F.data == "intro_item_done")

async def finish_intro_items(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    current_category = data.get("current_intro_category")
    next_category = _get_next_intro_category(current_category)

    if next_category:
        await state.update_data(current_intro_category=next_category, intro_item_page=0)
        await _show_intro_category_items(callback, state, next_category)
        await callback.answer()
        return

    # Move to Real Estate section

    real_estate_text = (

        "4|11 🗽 Real Estate\n\n"

        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "

        "to host another resident in a separate room — this is where you can share it with the community.\n\n"

        "Please list only the properties you are willing to share within a mutual exchange of community resources."

    )



    await callback.message.edit_text(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))



    await state.set_state(Registration.real_estate_section)



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


@router.callback_query(Registration.real_estate_section, F.data == "re_sec_back")



async def back_from_re_section(callback: CallbackQuery, state: FSMContext):



    # Go back to intro section last step or start if skipped



    data = await state.get_data()



    selected = set(data.get("selected_intro_formats", []))





    # Check if intro was skipped (selected_intro_formats would be empty if we didn't go through it)



    # But selected is initialized to empty list in cmd_start.



    # A better check is if we have intro categories or if we can rely on selected_intro_formats being populated only if we went there.



    # However, if user went there but selected nothing? No, finish_intro_section requires selection.





    # If selected_intro_formats is empty, it means we likely skipped.



    if not selected:



        # Back to Intro Start



        intro_text = (



            "3|11 🤝🏻 Personal Introduction\n\n"



            "In almost every life story, there is a moment when someone opened a door for us.\n\n"



            "Here, you can describe the key people in your orbit — founders, creators, innovators, "



            "curators, thinkers, leaders whom you are willing to introduce to other community members.\n\n"



            "Titles are indicative. If your contact is a decision maker, list them in the closest category."



        )



        await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))



        await state.set_state(Registration.intro_section)



    else:



        # Back to Intro Format



        await callback.message.edit_text(



            "Intro Format\n\nSpecify the format of introduction you are comfortable with:",



            reply_markup=get_multiselect_keyboard( selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back")



        )



        await state.set_state(Registration.intro_format)





    await callback.answer()





# --- Real Estate Section ---





@router.callback_query(Registration.real_estate_section, F.data == "realestate_skip")



async def skip_realestate_section(callback: CallbackQuery, state: FSMContext):



    cars_text = (



        "5|11 🖤 Cars\n\n"



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



        "4|11 🗽 Real Estate\n\n"



        "Whether it's an apartment, a villa you use only part-time — or simply your space is spacious enough "



        "to host another resident in a separate room — this is where you can share it with the community.\n\n"



        "Please list only the properties you are willing to share within a mutual exchange of community resources."



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



        reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back", page=data.get("prop_type_page", 0), page_callback_prefix="prop_type_page")



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



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back", page=data.get("prop_type_page", 0), page_callback_prefix="prop_type_page"))



    await callback.answer()





@router.callback_query(Registration.property_type, F.data == "prop_type_done")



async def finish_property_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    if not data.get("selected_property_types", []):



        await callback.answer("Please select at least one type.", show_alert=True)



        return





    try:



        # Progress message



        msg = await callback.message.answer("wooo-hoo! \nyou\'re doing great \u2014 already completed a third! \U0001f44f\U0001f3fb just a little more to go.")



        await asyncio.sleep(4)



        await msg.delete()





        # Move to Cars section



        cars_text = (



            "5|11 \U0001f5a4 Cars\n\n"



            "Please provide information about the cars you are willing to make available to community residents.\n\n"



            "By sharing your car, you\'re offering more than just a vehicle \u2014 you\'re giving someone the chance "



            "to experience freedom, explore, and create new memories."



        )



        await callback.message.edit_text(cars_text, reply_markup=get_section_intro_keyboard("cars_start", "cars_skip", "cars_sec_back"))



        await state.set_state(Registration.cars_section)



    finally:



        pass



    await callback.answer()





@router.callback_query(Registration.cars_section, F.data == "cars_sec_back")



async def back_from_cars_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_property_types", []))



    await callback.message.edit_text(



        "Type of Property\n\nPlease select:",



        reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back", page=data.get("prop_type_page", 0), page_callback_prefix="prop_type_page")



    )



    await state.set_state(Registration.property_type)



    await callback.answer()





# --- Cars Section ---





@router.callback_query(Registration.cars_section, F.data == "cars_skip")



async def skip_cars_section(callback: CallbackQuery, state: FSMContext):



    equipment_text = (



        "6|11 🎧 Equipment\n\n"



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



        "5|11 🖤 Cars\n\n"



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





    selected = set(data.get("selected_vehicle_types", []))



    await callback.message.edit_text(



        "Please specify type of the vehicle:",



        reply_markup=get_multiselect_keyboard(VEHICLE_TYPES, selected, "car_type", "car_type_done", "car_type_back", page=data.get("car_type_page", 0), page_callback_prefix="car_type_page")



    )



    await state.set_state(Registration.car_info)



    await callback.answer()





@router.callback_query(Registration.car_info, F.data == "car_type_back")



async def back_from_car_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_car_cities", []))



    await callback.message.edit_text(



        "Location\n\nSelect your vehicle location:",



        reply_markup=get_cities_select_keyboard("car_city", "car_city_done", selected, "car_city_back")



    )



    await state.set_state(Registration.car_location)



    await callback.answer()





@router.callback_query(Registration.car_info, F.data.startswith("car_type:"))



async def toggle_vehicle_type(callback: CallbackQuery, state: FSMContext):



    item_hash = callback.data.split(":")[1]



    data = await state.get_data()



    selected = set(data.get("selected_vehicle_types", []))



    target_item = find_item_by_hash(VEHICLE_TYPES, item_hash)



    if target_item:



        if target_item in selected:



            selected.remove(target_item)



        else:



            selected.add(target_item)



        await state.update_data(selected_vehicle_types=list(selected))



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(VEHICLE_TYPES, selected, "car_type", "car_type_done", "car_type_back", page=data.get("car_type_page", 0), page_callback_prefix="car_type_page"))



    await callback.answer()





@router.callback_query(Registration.car_info, F.data == "car_type_done")



async def finish_vehicle_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected_types = data.get("selected_vehicle_types", [])





    if not selected_types:



        await callback.answer("Please select at least one type.", show_alert=True)



        return





    # Join types for display/storage (comma separated)



    car_info_str = ", ".join(selected_types)



    await state.update_data(car_info=car_info_str)





    # Move to Equipment section



    equipment_text = (



        "6|11 \U0001f3a7 Equipment\n\n"



        "Please provide information about the equipment you are willing to make available to community residents.\n\n"



        "By providing clear details about the resources you\'re open to sharing, you help the community grow stronger."



    )



    await callback.message.edit_text(equipment_text, reply_markup=get_section_intro_keyboard("equipment_start", "equipment_skip", "equip_sec_back"))



    await state.set_state(Registration.equipment_section)



    await callback.answer()





@router.callback_query(Registration.equipment_section, F.data == "equip_sec_back")



async def back_from_equip_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_vehicle_types", []))



    await callback.message.edit_text(



        "Please specify type of the vehicle:",



        reply_markup=get_multiselect_keyboard(VEHICLE_TYPES, selected, "car_type", "car_type_done", "car_type_back", page=data.get("car_type_page", 0), page_callback_prefix="car_type_page")



    )



    await state.set_state(Registration.car_info)



    await callback.answer()





# --- Equipment Section ---





@router.callback_query(Registration.equipment_section, F.data == "equipment_skip")



async def skip_equipment_section(callback: CallbackQuery, state: FSMContext):



    aircraft_text = (



        "7|11 🛩️ Aircrafts\n\n"



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



        "6|11 🎧 Equipment\n\n"



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



        reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back", page=data.get("equip_type_page", 0), page_callback_prefix="equip_type_page")



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



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back", page=data.get("equip_type_page", 0), page_callback_prefix="equip_type_page"))



    await callback.answer()





@router.callback_query(Registration.equipment_types, F.data == "equip_type_done")



async def finish_equipment_types(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    if not data.get("selected_equipment_types", []):



        await callback.answer("Please select at least one type.", show_alert=True)



        return





    aircraft_text = (



        "7|11 \U0001f6e9\ufe0f Aircrafts\n\n"



        "Please provide information about the aircraft you are willing to make available to community residents.\n\n"



        "By opening access to such a unique asset, you take a special role within the community \u2014 "



        "inspiring others, elevating shared values, and creating moments that simply cannot happen without you."



    )



    await callback.message.edit_text(aircraft_text, reply_markup=get_section_intro_keyboard("aircraft_start", "aircraft_skip", "air_sec_back"))



    await state.set_state(Registration.aircraft_section)



    await callback.answer()





@router.callback_query(Registration.aircraft_section, F.data == "air_sec_back")



async def back_from_air_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_equipment_types", []))



    await callback.message.edit_text(



        "Types of Equipment You Can Share\n\nSelect all that apply:",



        reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back", page=data.get("equip_type_page", 0), page_callback_prefix="equip_type_page")



    )



    await state.set_state(Registration.equipment_types)



    await callback.answer()





# --- Air Transport Section ---





@router.callback_query(Registration.aircraft_section, F.data == "aircraft_skip")



async def skip_aircraft_section(callback: CallbackQuery, state: FSMContext, db: Database):





    vessel_text = (



        "8|11 💎 Boats\n\n"



        "Please provide information about the vessels you are willing to make available to community residents.\n\n"



        "We don't measure value in feet, engines, or length. What we share here is not \"status\" — "



        "but experiences, freedom and the joy of being on the water together."



    )



    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))



    await state.set_state(Registration.vessel_section)



    await callback.answer()





@router.callback_query(Registration.aircraft_section, F.data == "aircraft_start")



async def start_aircraft_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_air_cities", []))



    await callback.message.edit_text("Location\n\nSelect aircraft location:", reply_markup=get_cities_select_keyboard("air_city", "air_city_done", selected, "air_city_back"))



    await state.set_state(Registration.aircraft_location)



    await callback.answer()





@router.callback_query(Registration.aircraft_location, F.data == "air_city_back")



async def back_from_air_city(callback: CallbackQuery, state: FSMContext):



    aircraft_text = (



        "7|11 🛩️ Aircrafts\n\n"



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



        reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back", page=data.get("air_type_page", 0), page_callback_prefix="air_type_page")



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



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back", page=data.get("air_type_page", 0), page_callback_prefix="air_type_page"))



    await callback.answer()





@router.callback_query(Registration.aircraft_type, F.data == "air_type_done")



async def finish_aircraft_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    if not data.get("selected_aircraft_types", []):



        await callback.answer("Please select at least one type.", show_alert=True)



        return







    vessel_text = (



        "8|11 \U0001f48e Boats\n\n"



        "Please provide information about the vessels you are willing to make available to community residents.\n\n"



        "We don\'t measure value in feet, engines, or length. What we share here is not \\\"status\\\" \u2014 "



        "but experiences, freedom and the joy of being on the water together."



    )



    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))



    await state.set_state(Registration.vessel_section)



    await callback.answer()





@router.callback_query(Registration.vessel_section, F.data == "vessel_sec_back")



async def back_from_vessel_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_aircraft_types", []))



    await callback.message.edit_text(



        "Type of Aircraft\n\nSelect:",



        reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back", page=data.get("air_type_page", 0), page_callback_prefix="air_type_page")



    )



    await state.set_state(Registration.aircraft_type)



    await callback.answer()





# --- Water Transport Section ---





@router.callback_query(Registration.vessel_section, F.data == "vessel_skip")



async def skip_vessel_section(callback: CallbackQuery, state: FSMContext):



    specialist_text = (



        "9|11 🩵 Specialists\n\n"



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



    await callback.message.edit_text("Location and Sailing Area:", reply_markup=get_vessel_locations_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))



    await state.set_state(Registration.vessel_location)



    await callback.answer()





@router.callback_query(Registration.vessel_location, F.data == "vessel_city_back")



async def back_from_vessel_location(callback: CallbackQuery, state: FSMContext):



    vessel_text = (



        "8|11 💎 Boats\n\n"



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



    city = find_item_by_hash(VESSEL_LOCATIONS, city_hash)



    if city:



        data = await state.get_data()



        selected = set(data.get("selected_vessel_cities", []))



        if city in selected:



            selected.remove(city)



        else:



            selected.add(city)



        await state.update_data(selected_vessel_cities=list(selected))



        await callback.message.edit_reply_markup(reply_markup=get_vessel_locations_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))



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



        reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back", page=data.get("vessel_type_page", 0), page_callback_prefix="vessel_type_page")



    )



    await state.set_state(Registration.vessel_type)



    await callback.answer()





@router.callback_query(Registration.vessel_type, F.data == "vessel_type_back")



async def back_from_vessel_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_vessel_cities", []))



    await callback.message.edit_text("Location and Sailing Area:", reply_markup=get_vessel_locations_keyboard("vessel_city", "vessel_city_done", selected, "vessel_city_back"))



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



        await callback.message.edit_reply_markup(reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back", page=data.get("vessel_type_page", 0), page_callback_prefix="vessel_type_page"))



    await callback.answer()





@router.callback_query(Registration.vessel_type, F.data == "vessel_type_done")



async def finish_vessel_type(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    if not data.get("selected_vessel_types", []):



        await callback.answer("Please select at least one type.", show_alert=True)



        return





    specialist_text = (



        "9|11 \U0001f499 Specialists\n\n"



        "Each of us has our own \\\"super-people\\\" \u2014 specialists who once saved the day, guided us through a challenge, "



        "brought clarity, or simply made life easier.\n\n"



        "Please list only those specialists you have personally worked with and can genuinely vouch for."



    )



    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))



    await state.set_state(Registration.specialist_section)



    await callback.answer()





@router.callback_query(Registration.specialist_section, F.data == "spec_sec_back")



async def back_from_spec_section(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    selected = set(data.get("selected_vessel_types", []))



    await callback.message.edit_text(



        "Type of Vessel\n\nSelect all that apply:",



        reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back", page=data.get("vessel_type_page", 0), page_callback_prefix="vessel_type_page")



    )



    await state.set_state(Registration.vessel_type)



    await callback.answer()





# --- Specialists Section ---





@router.callback_query(Registration.specialist_section, F.data == "specialist_skip")



async def skip_specialist_section(callback: CallbackQuery, state: FSMContext):



    artwork_text = (



        "10|11 🫧 Works of Art\n\n"



        "If you're an artist, photographer, or creator — and your work carries meaning and intention — "



        "this is a space to share it with the community.\n\n"



        "By offering your work to fellow residents, you let it find a home where it will be genuinely seen and appreciated."



    )



    await callback.message.edit_text(artwork_text, reply_markup=get_section_intro_keyboard("artwork_start", "artwork_skip", "art_sec_back"))



    await state.set_state(Registration.artwork_section)



    await callback.answer()





@router.callback_query(Registration.specialist_section, F.data == "specialist_start")



async def start_specialist_section(callback: CallbackQuery, state: FSMContext):

    # Start from first category, show items as single-select
    first_category = SPEC_CATEGORY_ORDER[0]
    await state.update_data(current_specialist_category=first_category, spec_item_page=0)
    category_name = SPECIALIST_CATEGORIES[first_category]["name"]
    next_cat = _get_next_spec_category(first_category)
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the specialist you can recommend:",
        reply_markup=get_category_single_select_keyboard(
            first_category, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
            page=0, page_callback_prefix="spec_item_page",
            next_category_callback="spec_next_cat" if next_cat else None,
        )
    )
    await state.set_state(Registration.specialist_items)

    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data == "spec_back_cat")

async def back_from_spec_items(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_category = data.get("current_specialist_category")

    if current_category in SPEC_CATEGORY_ORDER:
        idx = SPEC_CATEGORY_ORDER.index(current_category)
        if idx > 0:
            prev_category = SPEC_CATEGORY_ORDER[idx - 1]
            await state.update_data(current_specialist_category=prev_category, spec_item_page=0)
            category_name = SPECIALIST_CATEGORIES[prev_category]["name"]
            prev_prev = idx - 2 >= 0
            next_cat = _get_next_spec_category(prev_category)
            await callback.message.edit_text(
                f"Category: {category_name}\n\nSelect the specialist you can recommend:",
                reply_markup=get_category_single_select_keyboard(
                    prev_category, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
                    page=0, page_callback_prefix="spec_item_page",
                    next_category_callback="spec_next_cat" if next_cat else None,
                )
            )
            await callback.answer()
            return

    specialist_text = (
        "9|11 🩵 Specialists\n\n"
        "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "
        "brought clarity, or simply made life easier.\n\n"
        "Please list only those specialists you have personally worked with and can genuinely vouch for."
    )
    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
    await state.set_state(Registration.specialist_section)

    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data == "spec_next_cat")

async def next_spec_category(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_category = data.get("current_specialist_category")
    next_category = _get_next_spec_category(current_category)

    if next_category:
        await state.update_data(current_specialist_category=next_category, spec_item_page=0)
        category_name = SPECIALIST_CATEGORIES[next_category]["name"]
        next_next = _get_next_spec_category(next_category)
        await callback.message.edit_text(
            f"Category: {category_name}\n\nSelect the specialist you can recommend:",
            reply_markup=get_category_single_select_keyboard(
                next_category, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
                page=0, page_callback_prefix="spec_item_page",
                next_category_callback="spec_next_cat" if next_next else None,
            )
        )

    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data.startswith("spec_item_page:"))

async def page_specialist_items(callback: CallbackQuery, state: FSMContext):

    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    category_key = data.get("current_specialist_category")
    if not category_key:
        await callback.answer()
        return

    await state.update_data(spec_item_page=page)
    next_cat = _get_next_spec_category(category_key)
    await callback.message.edit_reply_markup(
        reply_markup=get_category_single_select_keyboard(
            category_key, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
            page=page, page_callback_prefix="spec_item_page",
            next_category_callback="spec_next_cat" if next_cat else None,
        )
    )
    await callback.answer()


@router.callback_query(Registration.specialist_items, F.data.startswith("spec_item:"))

async def select_specialist_item(callback: CallbackQuery, state: FSMContext):

    item_hash = callback.data.split(":")[1]
    data = await state.get_data()
    category_key = data.get("current_specialist_category")
    items_list = SPECIALIST_CATEGORIES.get(category_key, {}).get("items", [])
    target_item = find_item_by_hash(items_list, item_hash)

    if target_item:
        await state.update_data(selected_specialist_item=target_item)
        await callback.message.delete()
        await callback.message.answer(
            f"Specialist: {target_item}\n\nPlease type the full name or public working name:",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(Registration.specialist_name)

    await callback.answer()


@router.message(Registration.specialist_name, F.text)

async def process_specialist_name(message: Message, state: FSMContext):

    if message.text.strip() == "🔙 Back":
        # Go back to current category items
        data = await state.get_data()
        category_key = data.get("current_specialist_category", SPEC_CATEGORY_ORDER[0])
        category_name = SPECIALIST_CATEGORIES[category_key]["name"]
        next_cat = _get_next_spec_category(category_key)
        await message.answer(
            f"Category: {category_name}\n\nSelect the specialist you can recommend:",
            reply_markup=get_category_single_select_keyboard(
                category_key, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
                page=0, page_callback_prefix="spec_item_page",
                next_category_callback="spec_next_cat" if next_cat else None,
            )
        )
        await state.set_state(Registration.specialist_items)
        return

    await state.update_data(specialist_name=message.text)

    await message.answer("Contact\n\nSpecify one or more (Telegram | WhatsApp | Email | Website | Social media):", reply_markup=get_cancel_keyboard())

    await state.set_state(Registration.specialist_contact)


@router.message(Registration.specialist_contact, F.text)

async def process_specialist_contact(message: Message, state: FSMContext):

    if message.text.strip() == "🔙 Back":

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

    if message.text.strip() == "🔙 Back":

        await message.answer("Contact\n\nSpecify one or more (Telegram | WhatsApp | Email | Website | Social media):", reply_markup=get_cancel_keyboard())

        await state.set_state(Registration.specialist_contact)

        return

    referral = message.text if message.text != "-" else ""

    await state.update_data(specialist_referral=referral)

    # Save current specialist to list
    data = await state.get_data()

    new_spec = {
        "category": data.get("current_specialist_category"),
        "item": data.get("selected_specialist_item"),
        "name": data.get("specialist_name"),
        "contact": data.get("specialist_contact"),
        "referral": referral
    }

    specialists_list = data.get("specialists_list", [])
    specialists_list.append(new_spec)
    await state.update_data(specialists_list=specialists_list)

    # Ask if user wants to add another specialist
    await message.answer(
        "Do you want to add another specialist?\n\nShare contacts of 3 people and get 1 free point for community exchanges 🩵",
        reply_markup=get_confirmation_keyboard("add_spec")
    )

    await state.set_state(Registration.specialist_loop_confirm)


@router.callback_query(Registration.specialist_loop_confirm, F.data.startswith("confirm:add_spec:"))

async def add_another_specialist(callback: CallbackQuery, state: FSMContext):

    # Loop back to first category
    first_category = SPEC_CATEGORY_ORDER[0]
    await state.update_data(current_specialist_category=first_category, spec_item_page=0)
    category_name = SPECIALIST_CATEGORIES[first_category]["name"]
    next_cat = _get_next_spec_category(first_category)
    await callback.message.edit_text(
        f"Category: {category_name}\n\nSelect the specialist you can recommend:",
        reply_markup=get_category_single_select_keyboard(
            first_category, SPECIALIST_CATEGORIES, "spec_item", "spec_back_cat",
            page=0, page_callback_prefix="spec_item_page",
            next_category_callback="spec_next_cat" if next_cat else None,
        )
    )

    await state.set_state(Registration.specialist_items)

    await callback.answer()





@router.callback_query(Registration.specialist_loop_confirm, F.data.startswith("cancel:add_spec"))



async def finish_specialist_loop(callback: CallbackQuery, state: FSMContext):



    # Move to Artworks section



    artwork_text = (



        "10|11 🫧 Works of Art\n\n"



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



            "9|11 🩵 Specialists\n\n"



            "Each of us has our own \"super-people\" — specialists who once saved the day, guided us through a challenge, "



            "brought clarity, or simply made life easier.\n\n"



            "Please list only those specialists you have personally worked with and can genuinely vouch for."



        )



        await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))



        await state.set_state(Registration.specialist_section)



    await callback.answer()





# --- Artworks Section ---





@router.callback_query(Registration.artwork_section, F.data == "artwork_skip")



async def skip_artwork_section(callback: CallbackQuery, state: FSMContext):

    maps_intro = (
        "11|11 🗺 Share Your Map\n\n"
        "In this section, you can share folder links to your favorite places on Google Maps.\n\n"
        "Before posting, please name the folder according to the city where the places are located "
        "and make sure there are no personal addresses.\n\n"
        "A few words about why this place is worth visiting would be great!"
    )
    await callback.message.edit_text(maps_intro, reply_markup=get_section_intro_keyboard("maps_start", "maps_skip", "maps_sec_back"))
    await state.set_state(Registration.maps_section)

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



        "10|11 🫧 Works of Art\n\n"



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





    await callback.message.delete()



    await callback.message.answer(



        "Author Name\nOr Pseudonym:",



        reply_markup=get_cancel_keyboard()



    )



    await state.set_state(Registration.art_author_name)



    await callback.answer()





@router.message(Registration.art_author_name, F.text)



async def process_art_author_name(message: Message, state: FSMContext):



    if message.text.strip() == "🔙 Back":



        await message.answer(



            "Form of Art\n\nSelect:",



            reply_markup=get_single_select_keyboard(ART_FORMS, "art_form", "art_form_back")



        )



        await state.set_state(Registration.art_form)



        return





    await state.update_data(art_author_name=message.text)





    # Skip location, go directly to photo



    await message.answer("Please add a link to your work (Instagram, Google Drive, etc.):", reply_markup=ReplyKeyboardRemove())



    await state.set_state(Registration.art_link)





@router.callback_query(Registration.art_location, F.data == "art_city_back")



async def back_from_art_city(callback: CallbackQuery, state: FSMContext):



    # Back to text input



    await callback.message.delete()



    await callback.message.answer(



        "Author Name\nOr Pseudonym:",



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



        # Update keyboard to show selection



        await callback.message.edit_reply_markup(



            reply_markup=get_cities_select_keyboard("art_city", "art_city_done", {city}, "art_city_back")



        )



    await callback.answer(f"Selected: {city}" if city else "")





@router.callback_query(Registration.art_location, F.data == "art_city_done")



async def finish_art_location(callback: CallbackQuery, state: FSMContext):



    data = await state.get_data()



    # Check if we need photo



    await callback.message.edit_text("Please add a link to your work (Instagram, Google Drive, etc.):")



    await state.set_state(Registration.art_link)



    await callback.answer()





@router.message(Registration.art_link, F.text)



async def process_art_link(message: Message, state: FSMContext, db: Database):



    if message.text.strip() == "🔙 Back":



        await message.answer(



            "Author Name\nOr Pseudonym:",



            reply_markup=get_cancel_keyboard()



        )



        await state.set_state(Registration.art_author_name)



        return



    



    # Save link



    await state.update_data(art_link=message.text.strip())





    # Move to Maps section



    maps_intro = (



        "11|11 🗺 Share Your Map\n\n"



        "In this section, you can share folder links to your favorite places on Google Maps.\n\n"



        "Before posting, please name the folder according to the city where the places are located "



        "and make sure there are no personal addresses.\n\n"



        "A few words about why this place is worth visiting would be great!"



    )



    await message.answer(maps_intro, reply_markup=get_section_intro_keyboard("maps_start", "maps_skip", "maps_sec_back"))



    await state.set_state(Registration.maps_section)





# --- Maps Section Handlers ---





@router.callback_query(Registration.maps_section, F.data == "maps_sec_back")



async def back_from_maps_section(callback: CallbackQuery, state: FSMContext):



    # Back to art photo



    await callback.message.delete()



    await callback.message.answer("Please add a link to your work (Instagram, Google Drive, etc.):", reply_markup=ReplyKeyboardRemove())



    await state.set_state(Registration.art_link)



    await callback.answer()





@router.callback_query(Registration.maps_section, F.data == "maps_skip")



async def skip_maps_section(callback: CallbackQuery, state: FSMContext, db: Database):



    await callback.message.delete()



    await finish_registration(callback.message, callback.from_user, state, db)



    await callback.answer()





@router.callback_query(Registration.maps_section, F.data == "maps_start")



async def start_maps_section(callback: CallbackQuery, state: FSMContext):

    # Initialize maps list
    await state.update_data(user_maps=[])

    await callback.message.delete()
    await callback.message.answer(
        "Enter the city for your map:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.maps_city)

    await callback.answer()


@router.message(Registration.maps_city, F.text)

async def process_maps_city_text(message: Message, state: FSMContext):

    if message.text.strip() == "🔙 Back":
        maps_intro = (
            "11|11 🗺 Share Your Map\n\n"
            "In this section, you can share folder links to your favorite places on Google Maps.\n\n"
            "Before posting, please name the folder according to the city where the places are located "
            "and make sure there are no personal addresses.\n\n"
            "A few words about why this place is worth visiting would be great!"
        )
        await message.answer(maps_intro, reply_markup=get_section_intro_keyboard("maps_start", "maps_skip", "maps_sec_back"))
        await state.set_state(Registration.maps_section)
        return

    city = message.text.strip()
    await state.update_data(current_map_city=city)

    await message.answer(
        f"City: {city}\n\nNow send the Google Maps link:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.maps_link)


@router.message(Registration.maps_link, F.text)



async def process_maps_link(message: Message, state: FSMContext, db: Database):



    if message.text.strip() == "🔙 Back":

        await message.answer(
            "Enter the city for your map:",
            reply_markup=get_cancel_keyboard()
        )

        await state.set_state(Registration.maps_city)

        return





    link = message.text.strip()



    data = await state.get_data()



    city = data.get("current_map_city", "Unknown")



    user_maps = data.get("user_maps", [])



    



    # Add map to list



    user_maps.append({"city": city, "link": link})



    await state.update_data(user_maps=user_maps)





    # Ask if want to add more



    from aiogram.utils.keyboard import InlineKeyboardBuilder



    builder = InlineKeyboardBuilder()



    builder.row(InlineKeyboardButton(text="➕ Add another map", callback_data="maps_add_more"))



    builder.row(InlineKeyboardButton(text="✅ Done", callback_data="maps_done"))



    



    await message.answer(



        f"✅ Map added: {city}\n\nWould you like to add another map?",



        reply_markup=builder.as_markup()



    )



    await state.set_state(Registration.maps_add_more)





@router.callback_query(Registration.maps_add_more, F.data == "maps_add_more")

async def add_more_maps(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await callback.message.answer(
        "Enter the city for your map:",
        reply_markup=get_cancel_keyboard()
    )

    await state.set_state(Registration.maps_city)

    await callback.answer()





@router.callback_query(Registration.maps_add_more, F.data == "maps_done")



async def finish_maps_section(callback: CallbackQuery, state: FSMContext, db: Database):



    await callback.message.delete()



    await finish_registration(callback.message, callback.from_user, state, db)



    await callback.answer()





async def finish_registration(message: Message, user: User, state: FSMContext, db: Database):



    data = await state.get_data()





    user_id = user.id



    name = data.get("name", "Unknown")



    # main_city is stored as string in state if we joined it?



    # In process_main_city, we did: main_city_str = ", ".join(selected_cities)



    main_city = data.get("main_city", "Unknown")





    current_city = main_city # Default to main



    about = data.get("about", "-")



    instagram = data.get("instagram", "-")



    username = user.username





    # Save user to DB



    success = await db.add_user(



        user_id=user_id,



        username=username,



        name=name,



        main_city=main_city,



        current_city=current_city,



        about=about,



        instagram=instagram



    )





    if success:



        # Save answers



        await db.add_user_answer(user_id, "registration_data", json.dumps(data, default=str))





        summary = (



            f"⚫️ Registration completed!\n\n"



            f"Name: {name}\n"



            f"City: {main_city}\n"



            f"About: {about}\n"



            f"Instagram: {instagram}\n"



            f"Points: 0"



        )





        await message.answer(summary, reply_markup=get_main_menu_keyboard())



        await state.clear()



    else:



        await message.answer("❌ Error saving registration data. Please try again or contact admin.", reply_markup=get_main_menu_keyboard())



        # We don't clear state so they can retry? Or we clear and they start over?



        # If add_user fails, it's a system error.



        await state.clear()
