"""Fix 2: Replace second welcome text + verify syntax"""
import pathlib
import py_compile

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()
data = data.replace(b'\r\r\n', b'\r\n')
content = data.decode('utf-8')

# Check if there's still a second instance of the welcome text
if 'hi luv! and welcome to joyseekers' in content:
    # Find and replace the second occurrence (in process_name back handler)
    idx = content.find('hi luv! and welcome to joyseekers')
    # Find the start of the intro_text block
    block_start = content.rfind('intro_text = (', 0, idx)
    # Find the end (the await message.answer line)
    await_end = content.find('await message.answer(intro_text, reply_markup=keyboard)', block_start)
    line_end = content.find('\r\n', await_end) + 2
    
    old_block = content[block_start:line_end]
    
    new_block = (
        '# Send welcome images as media group\r\n'
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
    
    content = content[:block_start] + new_block + content[line_end:]
    print("Replaced second welcome text (back handler)")
else:
    print("No remaining welcome text found - good!")

f.write_text(content, encoding='utf-8')

# Verify syntax
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
