"""
Update registration.py to send welcome images as media group
instead of text welcome message.
"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()
data = data.replace(b'\r\r\n', b'\r\n')
content = data.decode('utf-8')

# 1. Add InputMediaPhoto and FSInputFile to imports
if 'InputMediaPhoto' not in content:
    content = content.replace(
        'from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User',
        'from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, User, InputMediaPhoto\nfrom aiogram.types.input_file import FSInputFile'
    )
    print("Added InputMediaPhoto and FSInputFile imports")

# 2. Add pathlib import if missing
if 'import pathlib' not in content:
    content = content.replace(
        'import hashlib',
        'import hashlib\nimport pathlib'
    )
    print("Added pathlib import")

# 3. Replace the welcome text block in process_initial_invite_code
# Old: sends intro_text with SOUNDS GOOD button
# New: sends 6 images as media group, then SOUNDS GOOD button

old_welcome = (
    '        intro_text = (\r\n'
    '\r\n'
    '            "hi luv! and welcome to joyseekers \U0001f499\\n\\n"\r\n'
    '\r\n'
    '            "you\'re now part of a closed community of people who travel, do what they love, grow \u2014 and support each other through shared resources and opportunities.\\n\\n"\r\n'
    '\r\n'
    '            "inside joyseekers you can connect worldwide, exchange skills, receive trusted introductions, explore real estate, and access shared assets like cars or equipment.\\n\\n"\r\n'
    '\r\n'
    '            "the system is simple:\\n"\r\n'
    '\r\n'
    '            "1 shared resource = 1 credit, which you can use to unlock something in return.\\n\\n"\r\n'
    '\r\n'
    '            "to get started, just fill out a short questionnaire and add what you\'re open to sharing.\\n"\r\n'
    '\r\n'
    '            "after a quick approval by me, all sections will be unlocked.\\n\\n"\r\n'
    '\r\n'
    '            "not everyone finds this space \u2014 and that\'s what makes it special.\\n"\r\n'
    '\r\n'
    '            "glad to be here with you.\\n"\r\n'
    '\r\n'
    '            "stay joyful \U0001f499\\n"\r\n'
    '\r\n'
    '            "xx Anna"\r\n'
    '\r\n'
    '        )\r\n'
    '\r\n'
    '        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])\r\n'
    '\r\n'
    '        await message.answer(intro_text, reply_markup=keyboard)\r\n'
)

new_welcome = (
    '        # Send welcome images as media group\r\n'
    '        images_dir = pathlib.Path(__file__).parent.parent / "images"\r\n'
    '        media = [\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "1.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "2.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "3.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "4.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "5.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "6.JPG")),\r\n'
    '        ]\r\n'
    '        await message.answer_media_group(media)\r\n'
    '\r\n'
    '        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])\r\n'
    '        await message.answer("\\u200b", reply_markup=keyboard)\r\n'
)

if old_welcome in content:
    content = content.replace(old_welcome, new_welcome)
    print("Replaced welcome text with media group")
else:
    print("WARNING: Could not find old welcome text!")
    # Debug
    idx = content.find("hi luv! and welcome to joyseekers")
    if idx >= 0:
        print(f"  Found intro text at index {idx}")
        # Show context
        print(f"  Context: ...{content[idx-20:idx+40]}...")

# 4. Also update the Back handler in process_name (same intro text)
old_back_welcome = (
    '        intro_text = (\r\n'
    '\r\n'
    '            "hi luv! and welcome to joyseekers \U0001f499\\n\\n"\r\n'
    '\r\n'
    '            "you\'re now part of a closed community of people who travel, do what they love, grow \u2014 and support each other through shared resources and opportunities.\\n\\n"\r\n'
    '\r\n'
    '            "inside joyseekers you can connect worldwide, exchange skills, receive trusted introductions, explore real estate, and access shared assets like cars or equipment.\\n\\n"\r\n'
    '\r\n'
    '            "the system is simple:\\n"\r\n'
    '\r\n'
    '            "1 shared resource = 1 credit, which you can use to unlock something in return.\\n\\n"\r\n'
    '\r\n'
    '            "to get started, just fill out a short questionnaire and add what you\'re open to sharing.\\n"\r\n'
    '\r\n'
    '            "after a quick approval by me, all sections will be unlocked.\\n\\n"\r\n'
    '\r\n'
    '            "not everyone finds this space \u2014 and that\'s what makes it special.\\n"\r\n'
    '\r\n'
    '            "glad to be here with you.\\n"\r\n'
    '\r\n'
    '            "stay joyful \U0001f499\\n"\r\n'
    '\r\n'
    '            "xx Anna"\r\n'
    '\r\n'
    '        )\r\n'
    '\r\n'
    '        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])\r\n'
    '\r\n'
    '        await message.answer(intro_text, reply_markup=keyboard)\r\n'
)

new_back_welcome = (
    '        # Send welcome images as media group\r\n'
    '        images_dir = pathlib.Path(__file__).parent.parent / "images"\r\n'
    '        media = [\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "1.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "2.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "3.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "4.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "5.JPG")),\r\n'
    '            InputMediaPhoto(media=FSInputFile(images_dir / "6.JPG")),\r\n'
    '        ]\r\n'
    '        await message.answer_media_group(media)\r\n'
    '\r\n'
    '        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="SOUNDS GOOD.", callback_data="intro_sounds_good")]])\r\n'
    '        await message.answer("\\u200b", reply_markup=keyboard)\r\n'
)

if old_back_welcome in content:
    content = content.replace(old_back_welcome, new_back_welcome)
    print("Replaced back-to-welcome handler too")
else:
    print("Back handler: not found (may have different format)")

f.write_text(content, encoding='utf-8')
print(f"\nDone! File size: {len(content)}")

# Verify syntax
import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
