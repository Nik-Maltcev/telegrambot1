import re

try:
    with open('d:/telegrambot1/bot/handlers/registration.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    if r'\n' in text:
        # The file has literal '\n' characters instead of newlines
        text = text.replace(r'\n', '\n')
        # Clean up excessive blank lines
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        with open('d:/telegrambot1/bot/handlers/registration.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("SUCCESS: Fixed registration.py syntax.")
    else:
        print("File seems to be fine already.")
except Exception as e:
    print(f"Error: {e}")
