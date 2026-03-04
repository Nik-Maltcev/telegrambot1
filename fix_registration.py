"""
Script to remove redundant questions from registration.py
Modifies FSM states, handlers, and rewires transitions.
"""
import pathlib
import re

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

content = f.read_text(encoding='utf-8')

# ============================================================
# 1. Fix imports - remove unused imports from form_data
# ============================================================
old_import = """from bot.form_data import (
    SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS, INTERACTION_FORMATS, RESULT_TYPES,
    CITIES, INTRO_CATEGORIES, INTRO_FORMATS,
    PROPERTY_TYPES, PROPERTY_USAGE_FORMAT, PROPERTY_DURATION, PROPERTY_CAPACITY,
    VEHICLE_TYPES, CAR_USAGE_CONDITIONS, CAR_DURATION, CAR_CONDITIONS, CAR_PASSENGERS,
    EQUIPMENT_TYPES, EQUIPMENT_ACCESS_FORMAT, EQUIPMENT_DURATION, EQUIPMENT_RESPONSIBILITY,
    AIRCRAFT_TYPES, AIRCRAFT_USAGE_FORMAT, AIRCRAFT_SAFETY, AIRCRAFT_EXPENSES,
    VESSEL_TYPES, VESSEL_USAGE_FORMAT, VESSEL_SAFETY, VESSEL_FINANCIAL, VESSEL_LOCATIONS,
    SPECIALIST_CATEGORIES, SPECIALIST_CONNECTION_TYPE,
    ART_FORMS, ART_AUTHOR_TYPE
)"""

new_import = """from bot.form_data import (
    SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS,
    CITIES, INTRO_CATEGORIES,
    PROPERTY_TYPES,
    VEHICLE_TYPES,
    EQUIPMENT_TYPES,
    AIRCRAFT_TYPES,
    VESSEL_TYPES, VESSEL_LOCATIONS,
    SPECIALIST_CATEGORIES, SPECIALIST_CONNECTION_TYPE,
    ART_FORMS
)"""

content = content.replace(old_import, new_import)

# ============================================================
# 2. Remove FSM states
# ============================================================
states_to_remove = [
    '    interaction_format = State()\n',
    '    result_type = State()\n',
    '    intro_format = State()\n',
    '    property_usage = State()\n',
    '    property_duration = State()\n',
    '    property_capacity = State()\n',
    '    car_usage = State()\n',
    '    car_duration = State()\n',
    '    car_conditions = State()\n',
    '    car_passengers = State()\n',
    '    equipment_access = State()\n',
    '    equipment_duration = State()\n',
    '    equipment_responsibility = State()\n',
    '    aircraft_usage = State()\n',
    '    aircraft_safety = State()\n',
    '    aircraft_expenses = State()\n',
    '    vessel_usage = State()\n',
    '    vessel_safety = State()\n',
    '    vessel_financial = State()\n',
    '    art_author = State()\n',
]

for state in states_to_remove:
    content = content.replace(state, '')

# ============================================================
# 3. Clean up state initialization in process_initial_invite_code
# ============================================================
content = content.replace(
    "            selected_interaction_formats=[], selected_result_types=[],\n",
    ""
)
content = content.replace(
    "            selected_intro_items=[], selected_intro_formats=[],\n",
    "            selected_intro_items=[],\n"
)
content = content.replace(
    "            selected_equipment_access=[], selected_equipment_responsibility=[],\n",
    ""
)
content = content.replace(
    "            selected_aircraft_safety=[], selected_aircraft_expenses=[],\n",
    ""
)
content = content.replace(
    "            selected_vessel_safety=[], selected_vessel_financial=[],\n",
    ""
)

# ============================================================
# 4. SKILLS: finish_offer_formats -> go to Intro section (skip interaction_format & result_type)
# ============================================================

# Replace finish_offer_formats to go directly to Intro section
old_finish_offer = '''@router.callback_query(Registration.offer_formats, F.data == "q_fmt_done")
async def finish_offer_formats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_offer_formats", [])
    if not selected_items:
        await callback.answer("Please select at least one format.", show_alert=True)
        return

    selected = set(data.get("selected_interaction_formats", []))
    await callback.message.edit_text(
        "Interaction Format\\n\\nHow do you prefer to interact with community members?",
        reply_markup=get_multiselect_keyboard(INTERACTION_FORMATS, selected, "q_int", "q_int_done", "q_int_back")
    )
    await state.set_state(Registration.interaction_format)
    await callback.answer()'''

new_finish_offer = '''@router.callback_query(Registration.offer_formats, F.data == "q_fmt_done")
async def finish_offer_formats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_items = data.get("selected_offer_formats", [])
    if not selected_items:
        await callback.answer("Please select at least one format.", show_alert=True)
        return

    # Move to Personal Introductions section
    intro_text = (
        "2|10 \\U0001f91d\\U0001f3fb Personal Introduction\\n\\n"
        "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"
        "Here, you can describe the key people in your orbit \\u2014 founders, creators, innovators, "
        "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"
        "Sharing information about them does not commit you to making an introduction."
    )
    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))
    await state.set_state(Registration.intro_section)
    await callback.answer()'''

content = content.replace(old_finish_offer, new_finish_offer)

# Remove all interaction_format and result_type handlers (lines ~494-595)
# Remove back_from_interaction_format handler
content = re.sub(
    r'@router\.callback_query\(Registration\.interaction_format, F\.data == "q_int_back"\)\n'
    r'async def back_from_interaction_format\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '', content, count=1
)

# Remove toggle_interaction_format handler
content = re.sub(
    r'\n@router\.callback_query\(Registration\.interaction_format, F\.data\.startswith\("q_int:"\)\)\n'
    r'async def toggle_interaction_format\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

# Remove finish_interaction_formats handler
content = re.sub(
    r'\n@router\.callback_query\(Registration\.interaction_format, F\.data == "q_int_done"\)\n'
    r'async def finish_interaction_formats\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

# Remove back_from_result_type handler
content = re.sub(
    r'@router\.callback_query\(Registration\.result_type, F\.data == "q_res_back"\)\n'
    r'async def back_from_result_type\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '', content, count=1
)

# Remove toggle_result_type handler
content = re.sub(
    r'\n@router\.callback_query\(Registration\.result_type, F\.data\.startswith\("q_res:"\)\)\n'
    r'async def toggle_result_type\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

# Remove finish_skills_section (was result_type done handler)
content = re.sub(
    r'\n@router\.callback_query\(Registration\.result_type, F\.data == "q_res_done"\)\n'
    r'async def finish_skills_section\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

# Remove back_to_result_type handler
content = re.sub(
    r'@router\.callback_query\(Registration\.intro_section, F\.data == "intro_sec_back"\)\n'
    r'async def back_to_result_type\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '', content, count=1
)

# Add new intro_sec_back handler that goes back to offer_formats
intro_sec_back_new = '''@router.callback_query(Registration.intro_section, F.data == "intro_sec_back")
async def back_to_offer_formats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_offer_formats", []))
    await callback.message.edit_text(
        "Formats You Offer\\n\\nSelect the formats in which you can share your expertise:\\nYou can select multiple",
        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back")
    )
    await state.set_state(Registration.offer_formats)
    await callback.answer()


'''

# Insert the new handler right before the Personal Introductions Section comment
content = content.replace(
    '# --- Personal Introductions Section ---\n',
    intro_sec_back_new + '# --- Personal Introductions Section ---\n'
)

# ============================================================
# 5. INTROS: finish_intro_items -> go to Real Estate (skip intro_format)
# ============================================================

# Replace finish_intro_items to go directly to Real Estate
old_finish_intro_items = '''@router.callback_query(Registration.intro_items, F.data == "intro_item_done")
async def finish_intro_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_intro_items", []):
         await callback.answer("Please select at least one item.", show_alert=True)
         return

    # Skip location, go directly to format
    selected = set(data.get("selected_intro_formats", []))
    await callback.message.edit_text(
        "Intro Format\\n\\nSpecify the format of introduction you are comfortable with:",
        reply_markup=get_multiselect_keyboard(INTRO_FORMATS, selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back")
    )
    await state.set_state(Registration.intro_format)
    await callback.answer()'''

new_finish_intro_items = '''@router.callback_query(Registration.intro_items, F.data == "intro_item_done")
async def finish_intro_items(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_intro_items", []):
         await callback.answer("Please select at least one item.", show_alert=True)
         return

    # Move to Real Estate section
    real_estate_text = (
        "3|10 \\U0001f5fd Real Estate\\n\\n"
        "Whether it\\'s an apartment, a villa you use only part-time \\u2014 or simply your space is spacious enough "
        "to host another resident in a separate room \\u2014 this is where you can share it with the community.\\n\\n"
        "Please list only the properties you are willing to share free of charge."
    )
    await callback.message.edit_text(real_estate_text, reply_markup=get_section_intro_keyboard("realestate_start", "realestate_skip", "re_sec_back"))
    await state.set_state(Registration.real_estate_section)
    await callback.answer()'''

content = content.replace(old_finish_intro_items, new_finish_intro_items)

# Remove intro_format handlers: back_from_intro_format, toggle_intro_format, finish_intro_section
# Also remove finish_intro_location since it goes to intro_format

content = re.sub(
    r'@router\.callback_query\(Registration\.intro_format, F\.data == "intro_fmt_back"\)\n'
    r'async def back_from_intro_format\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '', content, count=1
)

content = re.sub(
    r'\n@router\.callback_query\(Registration\.intro_format, F\.data\.startswith\("intro_fmt:"\)\)\n'
    r'async def toggle_intro_format\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

content = re.sub(
    r'\n@router\.callback_query\(Registration\.intro_format, F\.data == "intro_fmt_done"\)\n'
    r'async def finish_intro_section\(.*?\n'
    r'(?:.*?\n)*?'
    r'    await callback\.answer\(\)\n',
    '\n', content, count=1
)

# Fix back_from_re_section: check selected_intro_items instead of selected_intro_formats
old_back_re = '''@router.callback_query(Registration.real_estate_section, F.data == "re_sec_back")
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
            "2|10 \\U0001f91d\\U0001f3fb Personal Introduction\\n\\n"
            "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"
            "Here, you can describe the key people in your orbit \\u2014 founders, creators, innovators, "
            "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"
            "Sharing information about them does not commit you to making an introduction."
        )
        await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))
        await state.set_state(Registration.intro_section)
    else:
        # Back to Intro Format
        await callback.message.edit_text(
            "Intro Format\\n\\nSpecify the format of introduction you are comfortable with:",
            reply_markup=get_multiselect_keyboard(INTRO_FORMATS, selected, "intro_fmt", "intro_fmt_done", "intro_fmt_back")
        )
        await state.set_state(Registration.intro_format)

    await callback.answer()'''

new_back_re = '''@router.callback_query(Registration.real_estate_section, F.data == "re_sec_back")
async def back_from_re_section(callback: CallbackQuery, state: FSMContext):
    # Go back to intro section start
    intro_text = (
        "2|10 \\U0001f91d\\U0001f3fb Personal Introduction\\n\\n"
        "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"
        "Here, you can describe the key people in your orbit \\u2014 founders, creators, innovators, "
        "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"
        "Sharing information about them does not commit you to making an introduction."
    )
    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))
    await state.set_state(Registration.intro_section)
    await callback.answer()'''

content = content.replace(old_back_re, new_back_re)

# ============================================================
# 6. REAL ESTATE: finish_property_type -> go to Cars (skip usage, duration, capacity)
# ============================================================

old_finish_prop_type = '''@router.callback_query(Registration.property_type, F.data == "prop_type_done")
async def finish_property_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_property_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    await callback.message.edit_text(
        "Usage Format\\n\\nChoose the suitable option:",
        reply_markup=get_single_select_keyboard(PROPERTY_USAGE_FORMAT, "prop_usage", "prop_usage_back")
    )
    await state.set_state(Registration.property_usage)
    await callback.answer()'''

new_finish_prop_type = '''@router.callback_query(Registration.property_type, F.data == "prop_type_done")
async def finish_property_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_property_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    try:
        # Progress message
        msg = await callback.message.answer("wooo-hoo! \\nyou\\'re doing great \\u2014 already completed a third! \\U0001f44f\\U0001f3fb just a little more to go.")
        await asyncio.sleep(4)
        await msg.delete()

        # Move to Cars section
        cars_text = (
            "4|10 \\U0001f5a4 Cars\\n\\n"
            "Please provide information about the cars you are willing to make available to community residents.\\n\\n"
            "By sharing your car, you\\'re offering more than just a vehicle \\u2014 you\\'re giving someone the chance "
            "to experience freedom, explore, and create new memories."
        )
        await callback.message.edit_text(cars_text, reply_markup=get_section_intro_keyboard("cars_start", "cars_skip", "cars_sec_back"))
        await state.set_state(Registration.cars_section)
    finally:
        pass
    await callback.answer()'''

content = content.replace(old_finish_prop_type, new_finish_prop_type)

# Remove property_usage, property_duration, property_capacity handlers
# back_from_prop_usage, select_property_usage, back_from_prop_duration, select_property_duration
# back_from_prop_capacity, select_property_capacity
for func_name in ['back_from_prop_usage', 'select_property_usage',
                   'back_from_prop_duration', 'select_property_duration',
                   'back_from_prop_capacity', 'select_property_capacity']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix back_from_cars_section: go back to property_type instead of property_capacity
old_back_cars = '''@router.callback_query(Registration.cars_section, F.data == "cars_sec_back")
async def back_from_cars_section(callback: CallbackQuery, state: FSMContext):
    # Back to Property Capacity
    await callback.message.edit_text(
        "Capacity\\n\\nNumber of people who can comfortably stay:",
        reply_markup=get_single_select_keyboard(PROPERTY_CAPACITY, "prop_cap", "prop_cap_back")
    )
    await state.set_state(Registration.property_capacity)
    await callback.answer()'''

new_back_cars = '''@router.callback_query(Registration.cars_section, F.data == "cars_sec_back")
async def back_from_cars_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_property_types", []))
    await callback.message.edit_text(
        "Type of Property\\n\\nPlease select:",
        reply_markup=get_multiselect_keyboard(PROPERTY_TYPES, selected, "prop_type", "prop_type_done", "prop_type_back")
    )
    await state.set_state(Registration.property_type)
    await callback.answer()'''

content = content.replace(old_back_cars, new_back_cars)

# ============================================================
# 7. CARS: finish_vehicle_type -> go to Equipment (skip usage, duration, conditions, passengers)
# ============================================================

old_finish_vehicle = '''@router.callback_query(Registration.car_info, F.data == "car_type_done")
async def finish_vehicle_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_types = data.get("selected_vehicle_types", [])

    if not selected_types:
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    # Join types for display/storage (comma separated)
    car_info_str = ", ".join(selected_types)
    await state.update_data(car_info=car_info_str)

    await callback.message.edit_text(
        "Usage Conditions\\n\\nChoose one:",
        reply_markup=get_single_select_keyboard(CAR_USAGE_CONDITIONS, "car_usage", "car_usage_back")
    )
    await state.set_state(Registration.car_usage)
    await callback.answer()'''

new_finish_vehicle = '''@router.callback_query(Registration.car_info, F.data == "car_type_done")
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
        "5|10 \\U0001f3a7 Equipment\\n\\n"
        "Please provide information about the equipment you are willing to make available to community residents.\\n\\n"
        "By providing clear details about the resources you\\'re open to sharing, you help the community grow stronger."
    )
    await callback.message.edit_text(equipment_text, reply_markup=get_section_intro_keyboard("equipment_start", "equipment_skip", "equip_sec_back"))
    await state.set_state(Registration.equipment_section)
    await callback.answer()'''

content = content.replace(old_finish_vehicle, new_finish_vehicle)

# Remove car_usage, car_duration, car_conditions, car_passengers handlers
for func_name in ['back_from_car_usage', 'select_car_usage',
                   'back_from_car_duration', 'select_car_duration',
                   'back_from_car_conditions', 'toggle_car_condition', 'finish_car_conditions',
                   'back_from_car_passengers', 'select_car_passengers']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix back_from_equip_section: go back to car_info (vehicle types) instead of car_passengers
old_back_equip = '''@router.callback_query(Registration.equipment_section, F.data == "equip_sec_back")
async def back_from_equip_section(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Maximum Passengers:",
        reply_markup=get_single_select_keyboard(CAR_PASSENGERS, "car_pass", "car_pass_back")
    )
    await state.set_state(Registration.car_passengers)
    await callback.answer()'''

new_back_equip = '''@router.callback_query(Registration.equipment_section, F.data == "equip_sec_back")
async def back_from_equip_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vehicle_types", []))
    await callback.message.edit_text(
        "Please specify type of the vehicle:",
        reply_markup=get_multiselect_keyboard(VEHICLE_TYPES, selected, "car_type", "car_type_done", "car_type_back")
    )
    await state.set_state(Registration.car_info)
    await callback.answer()'''

content = content.replace(old_back_equip, new_back_equip)

# ============================================================
# 8. EQUIPMENT: finish_equipment_types -> go to Air (skip access, duration, responsibility)
# ============================================================

old_finish_equip_types = '''@router.callback_query(Registration.equipment_types, F.data == "equip_type_done")
async def finish_equipment_types(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equipment_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    selected = set(data.get("selected_equipment_access", []))
    await callback.message.edit_text(
        "Equipment Access Format\\n\\nChoose one or multiple:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_ACCESS_FORMAT, selected, "equip_acc", "equip_acc_done", "equip_acc_back")
    )
    await state.set_state(Registration.equipment_access)
    await callback.answer()'''

new_finish_equip_types = '''@router.callback_query(Registration.equipment_types, F.data == "equip_type_done")
async def finish_equipment_types(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_equipment_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    aircraft_text = (
        "6|10 \\U0001f6e9\\ufe0f Aircrafts\\n\\n"
        "Please provide information about the aircraft you are willing to make available to community residents.\\n\\n"
        "By opening access to such a unique asset, you take a special role within the community \\u2014 "
        "inspiring others, elevating shared values, and creating moments that simply cannot happen without you."
    )
    await callback.message.edit_text(aircraft_text, reply_markup=get_section_intro_keyboard("aircraft_start", "aircraft_skip", "air_sec_back"))
    await state.set_state(Registration.aircraft_section)
    await callback.answer()'''

content = content.replace(old_finish_equip_types, new_finish_equip_types)

# Remove equipment_access, equipment_duration, equipment_responsibility handlers
for func_name in ['back_from_equip_access', 'toggle_equipment_access', 'finish_equipment_access',
                   'back_from_equip_duration', 'select_equipment_duration',
                   'back_from_equip_resp', 'toggle_equipment_responsibility', 'finish_equipment_section']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix back_from_air_section: go back to equipment_types instead of equipment_responsibility
old_back_air = '''@router.callback_query(Registration.aircraft_section, F.data == "air_sec_back")
async def back_from_air_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equipment_responsibility", []))
    await callback.message.edit_text(
        "Responsibility and Safety:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_RESPONSIBILITY, selected, "equip_resp", "equip_resp_done", "equip_resp_back")
    )
    await state.set_state(Registration.equipment_responsibility)
    await callback.answer()'''

new_back_air = '''@router.callback_query(Registration.aircraft_section, F.data == "air_sec_back")
async def back_from_air_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_equipment_types", []))
    await callback.message.edit_text(
        "Types of Equipment You Can Share\\n\\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(EQUIPMENT_TYPES, selected, "equip_type", "equip_type_done", "equip_type_back")
    )
    await state.set_state(Registration.equipment_types)
    await callback.answer()'''

content = content.replace(old_back_air, new_back_air)

# ============================================================
# 9. AIR: finish_aircraft_type -> go to Boats (skip usage, safety, expenses)
# ============================================================

old_finish_air_type = '''@router.callback_query(Registration.aircraft_type, F.data == "air_type_done")
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
    await callback.answer()'''

new_finish_air_type = '''@router.callback_query(Registration.aircraft_type, F.data == "air_type_done")
async def finish_aircraft_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_aircraft_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    await callback.message.answer("complete the questionnaire carefully and you\\'ll receive 1 point to exchange within the community \\U0001f499")

    vessel_text = (
        "7|10 \\U0001f48e Boats\\n\\n"
        "Please provide information about the vessels you are willing to make available to community residents.\\n\\n"
        "We don\\'t measure value in feet, engines, or length. What we share here is not \\\\\\"status\\\\\\" \\u2014 "
        "but experiences, freedom and the joy of being on the water together."
    )
    await callback.message.edit_text(vessel_text, reply_markup=get_section_intro_keyboard("vessel_start", "vessel_skip", "vessel_sec_back"))
    await state.set_state(Registration.vessel_section)
    await callback.answer()'''

content = content.replace(old_finish_air_type, new_finish_air_type)

# Remove aircraft_usage, aircraft_safety, aircraft_expenses handlers
for func_name in ['back_from_air_usage', 'select_aircraft_usage',
                   'back_from_air_safety', 'toggle_aircraft_safety', 'finish_aircraft_safety',
                   'back_from_air_expenses', 'toggle_aircraft_expenses', 'finish_aircraft_section']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix back_from_vessel_section: go back to aircraft_type instead of aircraft_expenses
old_back_vessel = '''@router.callback_query(Registration.vessel_section, F.data == "vessel_sec_back")
async def back_from_vessel_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_expenses", []))
    await callback.message.edit_text(
        "Expense Coverage:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_EXPENSES, selected, "air_exp", "air_exp_done", "air_exp_back")
    )
    await state.set_state(Registration.aircraft_expenses)
    await callback.answer()'''

new_back_vessel = '''@router.callback_query(Registration.vessel_section, F.data == "vessel_sec_back")
async def back_from_vessel_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_aircraft_types", []))
    await callback.message.edit_text(
        "Type of Aircraft\\n\\nSelect:",
        reply_markup=get_multiselect_keyboard(AIRCRAFT_TYPES, selected, "air_type", "air_type_done", "air_type_back")
    )
    await state.set_state(Registration.aircraft_type)
    await callback.answer()'''

content = content.replace(old_back_vessel, new_back_vessel)

# ============================================================
# 10. WATER: finish_vessel_type -> go to Specialists (skip usage, safety, financial)
# ============================================================

old_finish_vessel_type = '''@router.callback_query(Registration.vessel_type, F.data == "vessel_type_done")
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
    await callback.answer()'''

new_finish_vessel_type = '''@router.callback_query(Registration.vessel_type, F.data == "vessel_type_done")
async def finish_vessel_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("selected_vessel_types", []):
        await callback.answer("Please select at least one type.", show_alert=True)
        return

    specialist_text = (
        "8|10 \\U0001f499 Specialists\\n\\n"
        "Each of us has our own \\\\\\"super-people\\\\\\" \\u2014 specialists who once saved the day, guided us through a challenge, "
        "brought clarity, or simply made life easier.\\n\\n"
        "Please list only those specialists you have personally worked with and can genuinely vouch for."
    )
    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))
    await state.set_state(Registration.specialist_section)
    await callback.answer()'''

content = content.replace(old_finish_vessel_type, new_finish_vessel_type)

# Remove vessel_usage, vessel_safety, vessel_financial handlers
for func_name in ['back_from_vessel_usage', 'select_vessel_usage',
                   'back_from_vessel_safety', 'toggle_vessel_safety', 'finish_vessel_safety',
                   'back_from_vessel_fin', 'toggle_vessel_financial', 'finish_vessel_section']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix back_from_spec_section: go back to vessel_type instead of vessel_financial
old_back_spec = '''@router.callback_query(Registration.specialist_section, F.data == "spec_sec_back")
async def back_from_spec_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_financial", []))
    await callback.message.edit_text(
        "Financial Terms:",
        reply_markup=get_multiselect_keyboard(VESSEL_FINANCIAL, selected, "vessel_fin", "vessel_fin_done", "vessel_fin_back")
    )
    await state.set_state(Registration.vessel_financial)
    await callback.answer()'''

new_back_spec = '''@router.callback_query(Registration.specialist_section, F.data == "spec_sec_back")
async def back_from_spec_section(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_vessel_types", []))
    await callback.message.edit_text(
        "Type of Vessel\\n\\nSelect all that apply:",
        reply_markup=get_multiselect_keyboard(VESSEL_TYPES, selected, "vessel_type", "vessel_type_done", "vessel_type_back")
    )
    await state.set_state(Registration.vessel_type)
    await callback.answer()'''

content = content.replace(old_back_spec, new_back_spec)

# ============================================================
# 11. ARTWORKS: select_art_form -> go directly to art_author_name (skip art_author choice)
# ============================================================

old_select_art_form = '''@router.callback_query(Registration.art_form, F.data.startswith("art_form:"))
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
    await callback.answer()'''

new_select_art_form = '''@router.callback_query(Registration.art_form, F.data.startswith("art_form:"))
async def select_art_form(callback: CallbackQuery, state: FSMContext):
    item_hash = callback.data.split(":")[1]
    target_item = find_item_by_hash(ART_FORMS, item_hash)
    if target_item:
        await state.update_data(art_form=target_item)

    await callback.message.delete()
    await callback.message.answer(
        "Author Name\\nOr Pseudonym:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.art_author_name)
    await callback.answer()'''

content = content.replace(old_select_art_form, new_select_art_form)

# Remove art_author handlers: back_from_art_author, select_art_author
for func_name in ['back_from_art_author', 'select_art_author']:
    pattern = (r'@router\.callback_query\([^)]*\)\n'
               r'async def ' + func_name + r'\(.*?\n'
               r'(?:.*?\n)*?'
               r'    await callback\.answer\(\)\n')
    content = re.sub(pattern, '', content, count=1)

# Fix process_art_author_name back: go to art_form instead of art_author
old_art_back = '''    if message.text.strip() == "\\U0001f519 Back":
        await message.answer(
            "Who is the author?",
            reply_markup=get_single_select_keyboard(ART_AUTHOR_TYPE, "art_auth", "art_auth_back")
        )
        await state.set_state(Registration.art_author)
        return'''

new_art_back = '''    if message.text.strip() == "\\U0001f519 Back":
        await message.answer(
            "Form of Art\\n\\nSelect:",
            reply_markup=get_single_select_keyboard(ART_FORMS, "art_form", "art_form_back")
        )
        await state.set_state(Registration.art_form)
        return'''

content = content.replace(old_art_back, new_art_back)

# ============================================================
# 12. Clean up multiple consecutive blank lines
# ============================================================
content = re.sub(r'\n{4,}', '\n\n\n', content)

# Write back
f.write_text(content, encoding='utf-8')
print("SUCCESS: registration.py updated")

# Verify the state count
state_count = content.count('= State()')
print(f"Remaining FSM states: {state_count}")
