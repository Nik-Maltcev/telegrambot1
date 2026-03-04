"""
Fix registration.py to restore Type of Result question.
Handles the double-spaced format where every code line has a blank line after it.
"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

content = f.read_text(encoding='utf-8')

# 1. Add RESULT_TYPES to imports
if 'RESULT_TYPES' not in content:
    content = content.replace(
        " SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS, \r\n",
        " SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS, RESULT_TYPES,\r\n"
    )
    # Also try without trailing space/comma
    content = content.replace(
        " SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS,\r\n",
        " SKILL_CATEGORIES, ALL_SKILLS, OFFER_FORMATS, RESULT_TYPES,\r\n"
    )
    print("Added RESULT_TYPES to imports")

# 2. Add result_type state
if 'result_type = State()' not in content:
    content = content.replace(
        "    offer_formats = State()\r\n",
        "    offer_formats = State()\r\n    result_type = State()\r\n"
    )
    print("Added result_type state")

# 3. Modify finish_offer_formats: instead of going to intro, go to result_type
# Replace lines 820-840 (the body after the validation check)
old_body = (
    '\r\n'
    '    # Move to Personal Introductions section\r\n'
    '\r\n'
    '    intro_text = (\r\n'
    '\r\n'
    '        "2|10 \U0001f91d\U0001f3fb Personal Introduction\\n\\n"\r\n'
    '\r\n'
    '        "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"\r\n'
    '\r\n'
    '        "Here, you can describe the key people in your orbit \u2014 founders, creators, innovators, "\r\n'
    '\r\n'
    '        "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"\r\n'
    '\r\n'
    '        "Sharing information about them does not commit you to making an introduction."\r\n'
    '\r\n'
    '    )\r\n'
    '\r\n'
    '    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))\r\n'
    '\r\n'
    '    await state.set_state(Registration.intro_section)\r\n'
    '\r\n'
    '    await callback.answer()\r\n'
)

new_body = (
    '\r\n'
    '    # Move to Type of Result\r\n'
    '    selected = set(data.get("selected_result_types", []))\r\n'
    '    await callback.message.edit_text(\r\n'
    '        "Type of Result\\n\\nWhat kind of result can you provide?",\r\n'
    '        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back")\r\n'
    '    )\r\n'
    '    await state.set_state(Registration.result_type)\r\n'
    '    await callback.answer()\r\n'
)

if old_body in content:
    content = content.replace(old_body, new_body)
    print("Modified finish_offer_formats -> result_type")
else:
    print("WARNING: Could not find finish_offer_formats body to replace!")
    # Try to find nearby text
    idx = content.find("Move to Personal Introductions section")
    if idx > 0:
        print(f"  Found 'Move to Personal Introductions' at index {idx}")

# 4. Modify back_to_offer_formats (intro_sec_back) to go back to result_type
old_back = (
    '@router.callback_query(Registration.intro_section, F.data == "intro_sec_back")\r\n'
    '\r\n'
    'async def back_to_offer_formats(callback: CallbackQuery, state: FSMContext):\r\n'
    '\r\n'
    '    data = await state.get_data()\r\n'
    '\r\n'
    '    selected = set(data.get("selected_offer_formats", []))\r\n'
    '\r\n'
    '    await callback.message.edit_text(\r\n'
    '\r\n'
    '        "Formats You Offer\\n\\nSelect the formats in which you can share your expertise:\\nYou can select multiple",\r\n'
    '\r\n'
    '        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back")\r\n'
    '\r\n'
    '    )\r\n'
    '\r\n'
    '    await state.set_state(Registration.offer_formats)\r\n'
    '\r\n'
    '    await callback.answer()\r\n'
)

new_back = (
    '@router.callback_query(Registration.intro_section, F.data == "intro_sec_back")\r\n'
    'async def back_to_result_type(callback: CallbackQuery, state: FSMContext):\r\n'
    '    data = await state.get_data()\r\n'
    '    selected = set(data.get("selected_result_types", []))\r\n'
    '    await callback.message.edit_text(\r\n'
    '        "Type of Result\\n\\nWhat kind of result can you provide?",\r\n'
    '        reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back")\r\n'
    '    )\r\n'
    '    await state.set_state(Registration.result_type)\r\n'
    '    await callback.answer()\r\n'
)

if old_back in content:
    content = content.replace(old_back, new_back)
    print("Modified back_to_offer_formats -> back_to_result_type")
else:
    print("WARNING: Could not find back_to_offer_formats to replace!")

# 5. Insert result_type handlers before "# --- Personal Introductions Section ---"
result_handlers = (
    '\r\n'
    '@router.callback_query(Registration.result_type, F.data == "q_res_back")\r\n'
    'async def back_from_result_type(callback: CallbackQuery, state: FSMContext):\r\n'
    '    data = await state.get_data()\r\n'
    '    selected = set(data.get("selected_offer_formats", []))\r\n'
    '    await callback.message.edit_text(\r\n'
    '        "Formats You Offer\\n\\nSelect the formats in which you can share your expertise:\\nYou can select multiple",\r\n'
    '        reply_markup=get_multiselect_keyboard(OFFER_FORMATS, selected, "q_fmt", "q_fmt_done", "q_fmt_back")\r\n'
    '    )\r\n'
    '    await state.set_state(Registration.offer_formats)\r\n'
    '    await callback.answer()\r\n'
    '\r\n'
    '\r\n'
    '@router.callback_query(Registration.result_type, F.data.startswith("q_res:"))\r\n'
    'async def toggle_result_type(callback: CallbackQuery, state: FSMContext):\r\n'
    '    item_hash = callback.data.split(":")[1]\r\n'
    '    data = await state.get_data()\r\n'
    '    selected = set(data.get("selected_result_types", []))\r\n'
    '    target_item = find_item_by_hash(RESULT_TYPES, item_hash)\r\n'
    '    if target_item:\r\n'
    '        if target_item in selected:\r\n'
    '            selected.remove(target_item)\r\n'
    '        else:\r\n'
    '            selected.add(target_item)\r\n'
    '        await state.update_data(selected_result_types=list(selected))\r\n'
    '        await callback.message.edit_reply_markup(\r\n'
    '            reply_markup=get_multiselect_keyboard(RESULT_TYPES, selected, "q_res", "q_res_done", "q_res_back")\r\n'
    '        )\r\n'
    '    await callback.answer()\r\n'
    '\r\n'
    '\r\n'
    '@router.callback_query(Registration.result_type, F.data == "q_res_done")\r\n'
    'async def finish_result_type(callback: CallbackQuery, state: FSMContext):\r\n'
    '    data = await state.get_data()\r\n'
    '    if not data.get("selected_result_types", []):\r\n'
    '        await callback.answer("Please select at least one option.", show_alert=True)\r\n'
    '        return\r\n'
    '\r\n'
    '    # Move to Personal Introductions section\r\n'
    '    intro_text = (\r\n'
    '        "2|10 \U0001f91d\U0001f3fb Personal Introduction\\n\\n"\r\n'
    '        "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"\r\n'
    '        "Here, you can describe the key people in your orbit \u2014 founders, creators, innovators, "\r\n'
    '        "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"\r\n'
    '        "Sharing information about them does not commit you to making an introduction."\r\n'
    '    )\r\n'
    '    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))\r\n'
    '    await state.set_state(Registration.intro_section)\r\n'
    '    await callback.answer()\r\n'
    '\r\n'
    '\r\n'
)

marker = '# --- Personal Introductions Section ---\r\n'
if marker in content:
    content = content.replace(marker, result_handlers + marker)
    print("Inserted result_type handlers before intro section")
else:
    # Try alternative
    marker2 = '# --- Personal Introductions Section ---'
    if marker2 in content:
        content = content.replace(marker2, result_handlers.rstrip('\r\n') + '\r\n' + marker2)
        print("Inserted result_type handlers (alt marker)")
    else:
        print("WARNING: Could not find intro section marker!")

# Write back
f.write_text(content, encoding='utf-8')
print(f"\nDone! File size: {len(content)} chars")

# Verify
for name in ['RESULT_TYPES', 'result_type = State()', 'finish_result_type', 
             'toggle_result_type', 'back_from_result_type', 'back_to_result_type']:
    if name in content:
        print(f"  OK: {name}")
    else:
        print(f"  MISSING: {name}")
