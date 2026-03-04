"""Fix: ensure InputMediaPhoto and FSInputFile are imported"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()
data = data.replace(b'\r\r\n', b'\r\n')
content = data.decode('utf-8')

# Check current imports
if 'InputMediaPhoto' not in content:
    # Find the main aiogram.types import line
    old_import = 'from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User'
    if old_import in content:
        content = content.replace(
            old_import,
            old_import + ', InputMediaPhoto'
        )
        print("Added InputMediaPhoto to existing import")
    else:
        # Try to add as separate import after the first from aiogram.types line
        idx = content.find('from aiogram.types import')
        line_end = content.find('\r\n', idx)
        content = content[:line_end] + ', InputMediaPhoto' + content[line_end:]
        print("Added InputMediaPhoto (fallback)")

if 'FSInputFile' not in content:
    # Add after the aiogram.types import
    idx = content.find('from aiogram.types import')
    line_end = content.find('\r\n', idx) + 2
    content = content[:line_end] + 'from aiogram.types.input_file import FSInputFile\r\n' + content[line_end:]
    print("Added FSInputFile import")

f.write_text(content, encoding='utf-8')

import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
