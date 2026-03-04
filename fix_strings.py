import re

try:
    with open('d:/telegrambot1/bot/handlers/registration.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # The previous regex blindly replaced \n literals with real newlines,
    # which breaks multiline strings and f-strings that actually had \n text inside them.
    # To fix this, let's fix the specific f-strings that broke:
    
    text = text.replace('f"Your Telegram ID: `{message.from_user.id}`\n\n"\n\n        f"Admin IDs configured: {ADMIN_IDS}\n"\n\n        f"You are admin: {message.from_user.id in ADMIN_IDS}",', 'f"Your Telegram ID: `{message.from_user.id}`\\n"\\\n        f"Admin IDs configured: {ADMIN_IDS}\\n"\\\n        f"You are admin: {message.from_user.id in ADMIN_IDS}",')
    
    with open('d:/telegrambot1/bot/handlers/registration.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Fixed broken f-strings in registration.py.")

except Exception as e:
    print(f"Error: {e}")
