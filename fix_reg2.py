"""Fix remaining issues in registration.py:
1. Replace back_to_offer_formats with back_to_result_type
2. Fix \\r\\r\\n in newly inserted code
"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()

# Fix double \\r\\n
data = data.replace(b'\r\r\n', b'\r\n')

content = data.decode('utf-8')

# Replace back_to_offer_formats function
# It currently goes back to offer_formats, but should go to result_type
old_fn = (
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

new_fn = (
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

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("Replaced back_to_offer_formats -> back_to_result_type")
else:
    print("WARNING: Could not find back_to_offer_formats")
    # Debug
    idx = content.find('back_to_offer_formats')
    if idx >= 0:
        print(f"  Found at {idx}, context: {content[idx-50:idx+50]!r}")

f.write_text(content, encoding='utf-8')
print("Done!")

# Final check
for name in ['back_to_result_type', 'finish_result_type', 'toggle_result_type', 
             'back_from_result_type', 'RESULT_TYPES']:
    if name in content:
        print(f"  OK: {name}")
    else:
        print(f"  MISSING: {name}")
