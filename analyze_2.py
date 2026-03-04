import sys
# Redirect output to make it visible
original_stdout = sys.stdout
with open(r'd:\telegrambot1\output.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    
    with open(r'd:\telegrambot1\bot\handlers\registration.py', encoding='utf-8') as src:
        lines = src.readlines()
        
    print("=== MULTISELECT ===")
    for i, l in enumerate(lines, 1):
        if 'get_multiselect_keyboard' in l and 'import' not in l:
            print(f"{i}: {l.strip()}")
            
    print("\n=== CATEOGRY ITEMS ===")
    for i, l in enumerate(lines, 1):
        if 'get_category_items_keyboard' in l and 'import' not in l:
            print(f"{i}: {l.strip()}")
            
    print("\n=== CATEGORIES ===")
    for i, l in enumerate(lines, 1):
        if 'get_category_keyboard' in l and 'import' not in l:
            print(f"{i}: {l.strip()}")
            
sys.stdout = original_stdout
