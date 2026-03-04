"""Verify all modified files compile without errors"""
import py_compile
import pathlib
import sys

script_dir = pathlib.Path(__file__).parent
files = [
    script_dir / 'bot' / 'form_data.py',
    script_dir / 'bot' / 'keyboards.py',
    script_dir / 'bot' / 'handlers' / 'registration.py',
    script_dir / 'bot' / 'handlers' / 'resources.py',
    script_dir / 'bot' / 'handlers' / 'lots.py',
]

errors = 0
for f in files:
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"OK: {f.name}")
    except py_compile.PyCompileError as e:
        print(f"ERROR: {f.name}: {e}")
        errors += 1

if errors:
    print(f"\n{errors} file(s) have syntax errors!")
    sys.exit(1)
else:
    print("\nAll 5 files compile successfully!")
