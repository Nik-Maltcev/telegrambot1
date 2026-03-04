import ast
import sys

try:
    with open(r'd:\telegrambot1\bot\handlers\registration.py', encoding='utf-8') as f:
        ast.parse(f.read())
    print('registration.py: Syntax OK')
except SyntaxError as e:
    print(f'registration.py: Syntax ERROR: {e}')

try:
    with open(r'd:\telegrambot1\bot\form_data.py', encoding='utf-8') as f:
        ast.parse(f.read())
    print('form_data.py: Syntax OK')
except SyntaxError as e:
    print(f'form_data.py: Syntax ERROR: {e}')

# Also verify RESULT_TYPES is importable
sys.path.insert(0, r'd:\telegrambot1')
from bot.form_data import RESULT_TYPES
print(f'RESULT_TYPES: {RESULT_TYPES}')
