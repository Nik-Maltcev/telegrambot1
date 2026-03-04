import os
import pathlib

# Use the path relative to this script
script_dir = pathlib.Path(__file__).parent
f = script_dir / 'bot' / 'form_data.py'

data = f.read_bytes()

# Remove PROPERTY_USAGE_FORMAT block
s = data.find(b'PROPERTY_USAGE_FORMAT')
e = data.find(b'# --- Cars ---')
if s > 0 and e > s:
    ls = data.rfind(b'\n', 0, s) + 1
    data = data[:ls] + data[e:]
    f.write_bytes(data)
    print('OK: removed PROPERTY constants, new size:', len(data))
else:
    print('Already removed or not found')
