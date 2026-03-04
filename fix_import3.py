"""Fix imports using byte-level operations - handles \\r\\r\\n"""
import pathlib as _pl

f = _pl.Path(__file__).parent / 'bot' / 'handlers' / 'registration.py'
data = f.read_bytes()

# Work with bytes to handle \r\r\n properly
old_import = b'from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User'
new_import = b'from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User, InputMediaPhoto\r\nfrom aiogram.types.input_file import FSInputFile'

if b'InputMediaPhoto' not in data:
    data = data.replace(old_import, new_import)
    print("Added InputMediaPhoto + FSInputFile")
else:
    print("InputMediaPhoto already present")

if b'import pathlib' not in data:
    data = data.replace(b'import hashlib', b'import hashlib\r\nimport pathlib')
    print("Added pathlib")
else:
    print("pathlib already present")

f.write_bytes(data)

# Verify
import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")

# Double-check
content = f.read_bytes()
for name in [b'InputMediaPhoto', b'FSInputFile', b'import pathlib']:
    print(f"  {'OK' if name in content else 'MISS'}: {name.decode()}")
