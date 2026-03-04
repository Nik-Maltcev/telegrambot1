"""Fix double carriage returns in registration.py"""
import pathlib

script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'handlers' / 'registration.py'

data = f.read_bytes()
# Fix \r\r\n -> \r\n
data = data.replace(b'\r\r\n', b'\r\n')
# Also fix any \r\r that might remain
data = data.replace(b'\r\r', b'\r')
f.write_bytes(data)
print(f"Fixed line endings. Size: {len(data)}")
