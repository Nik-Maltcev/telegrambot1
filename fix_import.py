"""Fix: ensure pathlib is imported in registration.py"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()
data = data.replace(b'\r\r\n', b'\r\n')
content = data.decode('utf-8')

if 'import pathlib' not in content:
    # Add after 'import hashlib'
    content = content.replace(
        'import hashlib\r\n',
        'import hashlib\r\nimport pathlib\r\n'
    )
    print("Added import pathlib")
else:
    print("pathlib already imported")

f.write_text(content, encoding='utf-8')

import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
