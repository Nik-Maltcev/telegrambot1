"""Definitive fix for missing imports in registration.py"""
import pathlib
import sys

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

content_str = f.read_text(encoding='utf-8')

# The exact strings to check for (imports only!)
import1 = 'from aiogram.types import InputMediaPhoto'
import2 = 'from aiogram.types.input_file import FSInputFile'
import3 = 'import pathlib'

needs_import1 = import1 not in content_str
needs_import2 = import2 not in content_str
# pathlib was actually imported correctly because it was 'import pathlib'
# but let's just make sure it's at the top
needs_import3 = import3 not in content_str

if not needs_import1 and not needs_import2 and not needs_import3:
    print("All imports are already present as import statements!")
    sys.exit(0)

# We will inject the missing imports right after the very first line "from aiogram import Router, F"
new_imports = ""
if needs_import1:
    new_imports += import1 + "\n"
    print("Will add:", import1)
if needs_import2:
    new_imports += import2 + "\n"
    print("Will add:", import2)
if needs_import3:
    new_imports += import3 + "\n"
    print("Will add:", import3)

# Find where to inject
lines = content_str.splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith('from aiogram import Router'):
        lines.insert(i + 1, new_imports)
        break

f.write_text("".join(lines), encoding='utf-8')
print("Successfully inserted missing imports.")

# Verify syntax
import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
