"""Analyze all multiselect usages in registration.py"""
import re

f = open(r'd:\telegrambot1\bot\handlers\registration.py', encoding='utf-8').read()
lines = f.split('\n')

print("=== get_multiselect_keyboard usages ===")
for i, l in enumerate(lines, 1):
    if 'get_multiselect_keyboard' in l and 'import' not in l and l.strip():
        print(f"  Line {i}: {l.strip()[:130]}")

print("\n=== get_category_items_keyboard usages ===")
for i, l in enumerate(lines, 1):
    if 'get_category_items_keyboard' in l and 'import' not in l and l.strip():
        print(f"  Line {i}: {l.strip()[:130]}")

print("\n=== get_category_keyboard usages ===")
for i, l in enumerate(lines, 1):
    if 'get_category_keyboard' in l and 'import' not in l and l.strip():
        print(f"  Line {i}: {l.strip()[:130]}")

print("\n=== Item counts from form_data ===")
import sys
sys.path.insert(0, r'd:\telegrambot1')
from bot.form_data import *
print(f"  OFFER_FORMATS: {len(OFFER_FORMATS)} items")
print(f"  RESULT_TYPES: {len(RESULT_TYPES)} items")
print(f"  PROPERTY_TYPES: {len(PROPERTY_TYPES)} items")
print(f"  VEHICLE_TYPES: {len(VEHICLE_TYPES)} items")
print(f"  EQUIPMENT_TYPES: {len(EQUIPMENT_TYPES)} items")
print(f"  AIRCRAFT_TYPES: {len(AIRCRAFT_TYPES)} items")
print(f"  VESSEL_TYPES: {len(VESSEL_TYPES)} items")
print(f"  ALL_SKILLS: {len(ALL_SKILLS)} items")
total_intro = sum(len(v['items']) for v in INTRO_CATEGORIES.values())
print(f"  INTRO items (all categories): {total_intro} items")
total_spec = sum(len(v['items']) for v in SPECIALIST_CATEGORIES.values())
print(f"  SPECIALIST items (all categories): {total_spec} items")
print(f"  ART_FORMS: {len(ART_FORMS)} items")
