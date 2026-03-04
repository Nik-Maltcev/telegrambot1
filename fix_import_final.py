"""Foolproof fix for missing imports in registration.py"""
import pathlib
import sys

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

try:
    with open(f, 'r', encoding='utf-8') as file:
        lines = file.readlines()
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

content_str = "".join(lines)
has_input_media = 'InputMediaPhoto' in content_str
has_fsinput = 'FSInputFile' in content_str
has_pathlib = 'import pathlib' in content_str

if has_input_media and has_fsinput and has_pathlib:
    print("All imports already present!")
    sys.exit(0)

# Add missing imports to the very top, after the first import
new_lines = []
imports_added = False

for line in lines:
    new_lines.append(line)
    if line.startswith('from aiogram import Router') and not imports_added:
        if not has_input_media:
            new_lines.append("from aiogram.types import InputMediaPhoto\n")
            print("Added InputMediaPhoto")
            has_input_media = True
        
        if not has_fsinput:
            new_lines.append("from aiogram.types.input_file import FSInputFile\n")
            print("Added FSInputFile")
            has_fsinput = True
            
        if not has_pathlib:
            new_lines.append("import pathlib\n")
            print("Added import pathlib")
            has_pathlib = True
            
        imports_added = True

try:
    with open(f, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    print("File saved successfully.")
except Exception as e:
    print(f"Error writing file: {e}")
    sys.exit(1)

# Verify syntax
import py_compile
try:
    py_compile.compile(str(f), doraise=True)
    print("Syntax OK!")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
