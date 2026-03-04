"""Fix the invisible character in the message.answer that causes TelegramBadRequest"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

content_str = f.read_text(encoding='utf-8')

# We need to replace the two instances of await message.answer("\u200b", reply_markup=keyboard)
# with a visible text, e.g., "Press SOUNDS GOOD. to continue"

old_text = 'await message.answer("\\u200b", reply_markup=keyboard)'
new_text = 'await message.answer("👇 Click below to continue:", reply_markup=keyboard)'

if old_text in content_str:
    new_content = content_str.replace(old_text, new_text)
    f.write_text(new_content, encoding='utf-8')
    print("Fixed empty message issue in registration.py!")
else:
    print("Could not find the exact string:\\n", old_text)

import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
