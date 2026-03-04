"""
Second pass cleanup for registration.py
Uses line-by-line approach to handle \r\n properly
"""
import pathlib
import re

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

content = f.read_text(encoding='utf-8')

# Normalize line endings for regex
content = content.replace('\r\n', '\n')

# ============================================================
# 1. Fix imports (the old import block is still there)
# ============================================================
old_imports = [
    'INTERACTION_FORMATS, RESULT_TYPES,',
    'INTRO_FORMATS,',
    'PROPERTY_USAGE_FORMAT, PROPERTY_DURATION, PROPERTY_CAPACITY,',
    'CAR_USAGE_CONDITIONS, CAR_DURATION, CAR_CONDITIONS, CAR_PASSENGERS,',
    'EQUIPMENT_ACCESS_FORMAT, EQUIPMENT_DURATION, EQUIPMENT_RESPONSIBILITY,',
    'AIRCRAFT_USAGE_FORMAT, AIRCRAFT_SAFETY, AIRCRAFT_EXPENSES,',
    'VESSEL_USAGE_FORMAT, VESSEL_SAFETY, VESSEL_FINANCIAL,',
    'ART_AUTHOR_TYPE',
]

# Clean up imports line by line
for imp in old_imports:
    # Remove the import token + trailing comma/whitespace
    content = content.replace(imp + '\n', '\n')
    content = content.replace(' ' + imp, '')
    content = content.replace(imp, '')

# Clean up any resulting double commas, trailing commas, empty lines in import
content = re.sub(r',\s*,', ',', content)
content = re.sub(r',\s*\)', ')', content)
content = re.sub(r'\(\s*,', '(', content)

# Clean up the import block - remove empty lines within it
import_match = re.search(r'from bot\.form_data import \(.*?\)', content, re.DOTALL)
if import_match:
    import_text = import_match.group(0)
    # Remove blank lines within import
    clean_import = re.sub(r'\n\s*\n', '\n', import_text)
    # Remove double spaces
    clean_import = re.sub(r'  +', ' ', clean_import)
    content = content.replace(import_text, clean_import)

# ============================================================
# 2. Remove handler functions that still reference removed constants
# ============================================================

# Helper function to remove a complete handler function
def remove_handler(content, func_name):
    """Remove a complete @router decorated async def function"""
    # Pattern: @router... decorator line(s) + async def funcname + body until next @router or # ---
    pattern = (
        r'@router\.[^\n]+\n'
        r'async def ' + func_name + r'\([^)]*\):\n'
        r'(?:(?!@router\.|# ---)[^\n]*\n)*'
    )
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + content[match.end():]
        print(f"  Removed: {func_name}")
    else:
        print(f"  NOT FOUND: {func_name}")
    return content

# Functions that should have been removed but weren't
handlers_to_remove = [
    # Intro location handlers (unused since location was skipped)
    'finish_intro_location',
    # Property handlers
    'select_property_usage',
    'back_from_prop_duration',
    'select_property_duration',
    'back_from_prop_capacity',
    'select_property_capacity',
    # Car handlers
    'select_car_usage',
    'back_from_car_duration',
    'select_car_duration',
    'back_from_car_conditions',
    'toggle_car_condition',
    'finish_car_conditions',
    'back_from_car_passengers',
    'select_car_passengers',
    # Equipment handlers
    'toggle_equipment_access',
    'finish_equipment_access',
    'back_from_equip_duration',
    'select_equipment_duration',
    'back_from_equip_resp',
    'toggle_equipment_responsibility',
    'finish_equipment_section',
    # Aircraft handlers
    'select_aircraft_usage',
    'back_from_air_safety',
    'toggle_aircraft_safety',
    'finish_aircraft_safety',
    'back_from_air_expenses',
    'toggle_aircraft_expenses',
    'finish_aircraft_section',
    # Vessel handlers
    'select_vessel_usage',
    'back_from_vessel_safety',
    'toggle_vessel_safety',
    'finish_vessel_safety',
    'back_from_vessel_fin',
    'toggle_vessel_financial',
    'finish_vessel_section',
    # Art handlers
    'select_art_author',
    'back_from_art_author',
]

print("Removing handler functions:")
for func in handlers_to_remove:
    content = remove_handler(content, func)

# Also check for any remaining back handlers that reference removed states
# back_from_prop_usage
content = remove_handler(content, 'back_from_prop_usage')
content = remove_handler(content, 'back_from_car_usage')
content = remove_handler(content, 'back_from_equip_access')
content = remove_handler(content, 'back_from_air_usage')
content = remove_handler(content, 'back_from_vessel_usage')

# ============================================================
# 3. Fix remaining back handler for art_author_name
# ============================================================
# process_art_author_name back should go to art_form, not art_author
content = content.replace(
    '''    if message.text.strip() == "\U0001f519 Back":
        await message.answer(
            "Who is the author?",
            reply_markup=get_single_select_keyboard(ART_AUTHOR_TYPE, "art_auth", "art_auth_back")
        )
        await state.set_state(Registration.art_author)
        return''',
    '''    if message.text.strip() == "\U0001f519 Back":
        await message.answer(
            "Form of Art\\n\\nSelect:",
            reply_markup=get_single_select_keyboard(ART_FORMS, "art_form", "art_form_back")
        )
        await state.set_state(Registration.art_form)
        return'''
)

# ============================================================
# 4. Clean up consecutive blank lines
# ============================================================
content = re.sub(r'\n{4,}', '\n\n\n', content)

# Restore \r\n line endings
content = content.replace('\n', '\r\n')

f.write_text(content, encoding='utf-8')
print("\nSUCCESS: Second pass cleanup complete")

# Count remaining references
for name in ['INTERACTION_FORMATS', 'RESULT_TYPES', 'INTRO_FORMATS',
             'PROPERTY_USAGE_FORMAT', 'PROPERTY_DURATION', 'PROPERTY_CAPACITY',
             'CAR_USAGE_CONDITIONS', 'CAR_DURATION', 'CAR_CONDITIONS', 'CAR_PASSENGERS',
             'EQUIPMENT_ACCESS_FORMAT', 'EQUIPMENT_DURATION', 'EQUIPMENT_RESPONSIBILITY',
             'AIRCRAFT_USAGE_FORMAT', 'AIRCRAFT_SAFETY', 'AIRCRAFT_EXPENSES',
             'VESSEL_USAGE_FORMAT', 'VESSEL_SAFETY', 'VESSEL_FINANCIAL',
             'ART_AUTHOR_TYPE']:
    count = content.count(name)
    if count > 0:
        print(f"  WARNING: {name} still referenced {count} times")
