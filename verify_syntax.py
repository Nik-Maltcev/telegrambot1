"""Verify registration.py can be compiled without errors"""
import pathlib
import py_compile
import sys

script_dir = pathlib.Path(__file__).parent
reg_file = script_dir / 'bot' / 'handlers' / 'registration.py'
form_file = script_dir / 'bot' / 'form_data.py'
kb_file = script_dir / 'bot' / 'keyboards.py'

errors = []
for f in [form_file, kb_file, reg_file]:
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"OK: {f.name}")
    except py_compile.PyCompileError as e:
        print(f"ERROR: {f.name}: {e}")
        errors.append(str(e))

if errors:
    print(f"\n{len(errors)} file(s) have syntax errors!")
    sys.exit(1)
else:
    print("\nAll files compile successfully!")
