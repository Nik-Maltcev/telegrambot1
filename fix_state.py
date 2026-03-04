"""Definitive fix: add result_type state and fix line endings"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()

# 1. Fix all \r\r\n -> \r\n
data = data.replace(b'\r\r\n', b'\r\n')
content = data.decode('utf-8')

# 2. Add result_type = State() after offer_formats = State()
if 'result_type = State()' not in content:
    content = content.replace(
        '    offer_formats = State()\r\n',
        '    offer_formats = State()\r\n    result_type = State()\r\n'
    )
    print("Added result_type = State()")
else:
    print("result_type = State() already exists")

# 3. Verify
if 'result_type = State()' in content:
    print("VERIFIED: result_type state present")
else:
    print("ERROR: result_type state still missing!")
    # Try without \r\n
    content = content.replace(
        '    offer_formats = State()\n',
        '    offer_formats = State()\n    result_type = State()\n'
    )
    if 'result_type = State()' in content:
        print("Fixed with \\n only")

f.write_text(content, encoding='utf-8')
print(f"Done. File size: {len(content)}")
