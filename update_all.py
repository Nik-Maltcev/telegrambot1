"""
Comprehensive update script for the bot.
Updates: form_data.py, resources.py, keyboards.py, lots.py, registration.py
"""
import pathlib
import re

script_dir = pathlib.Path(__file__).parent
bot_dir = script_dir / 'bot'

# ============================================================
# 1. UPDATE form_data.py
# ============================================================
f = bot_dir / 'form_data.py'
content = f.read_text(encoding='utf-8')

# --- 1a. CITIES: Add new, remove old ---
# Remove Beijing, Sydney, Sao Paulo
content = content.replace('    "Shanghai \U0001f1e8\U0001f1f3", "Beijing \U0001f1e8\U0001f1f3", "Dubai \U0001f1e6\U0001f1ea",\r\n', '    "Shanghai \U0001f1e8\U0001f1f3", "Dubai \U0001f1e6\U0001f1ea",\r\n')
content = content.replace('    "Sydney \U0001f1e6\U0001f1fa", "Melbourne \U0001f1e6\U0001f1fa",\r\n', '    "Melbourne \U0001f1e6\U0001f1fa",\r\n')
content = content.replace(', "S\u00e3o Paulo \U0001f1e7\U0001f1f7"', '')

# Add new cities before the closing bracket
content = content.replace(
    '    "Baku \U0001f1e6\U0001f1ff", "Tbilisi \U0001f1ec\U0001f1ea"\r\n]',
    '    "Baku \U0001f1e6\U0001f1ff", "Tbilisi \U0001f1ec\U0001f1ea",\r\n'
    '    "Athens \U0001f1ec\U0001f1f7", "Marseille \U0001f1eb\U0001f1f7", "Belgrade \U0001f1f7\U0001f1f8", "Cape Town \U0001f1ff\U0001f1e6",\r\n'
    '    "Tulum \U0001f1f2\U0001f1fd", "Ubud \U0001f1ee\U0001f1e9", "Phuket \U0001f1f9\U0001f1ed", "Cannes/Nice \U0001f1eb\U0001f1f7",\r\n'
    '    "Venice \U0001f1ee\U0001f1f9", "Helsinki \U0001f1eb\U0001f1ee", "Tallinn \U0001f1ea\U0001f1ea"\r\n]'
)

# --- 1b. Add RESULT_TYPES back ---
# Insert after OFFER_FORMATS block
content = content.replace(
    'OFFER_FORMATS = [\r\n'
    '    "Professional consultations", "Access to courses / materials", "Educational practices",\r\n'
    '    "Workshops", "Professional coaching", "Individual programs",\r\n'
    '    "Project or task implementation"\r\n'
    ']\r\n\r\n\r\n',
    'OFFER_FORMATS = [\r\n'
    '    "Professional consultations", "Access to courses / materials", "Educational practices",\r\n'
    '    "Workshops", "Professional coaching", "Individual programs",\r\n'
    '    "Project or task implementation"\r\n'
    ']\r\n\r\n'
    'RESULT_TYPES = [\r\n'
    '    "Strategic clarity",\r\n'
    '    "Problem solving",\r\n'
    '    "Feedback / expert review",\r\n'
    '    "Optimization",\r\n'
    '    "Guidance and Support",\r\n'
    '    "Creative development"\r\n'
    ']\r\n\r\n'
)

# --- 1c. Property type rename ---
content = content.replace('"Room (shared living)"', '"Room in a shared home"')

# --- 1d. Specialist Categories overhaul ---
old_specialists = '''SPECIALIST_CATEGORIES = {
    "legal_finance": {
        "name": "Legalization & Finance",
        "items": [
            "Tax specialist",
            "US visas",
            "European residence permits",
            "Schengen visas",
            "Citizenship",
            "Business legalization abroad",
            "Legal services",
            "Real estate investments",
            "Investments for HNWIs",
            "Wealth management"
        ]
    },
    "health_body": {
        "name": "Health & Body",
        "items": [
            "Doctors and health specialists",
            "Body-performance specialists",
            "Psychologists, mental health coaches"
        ]
    },
    "health_energy": {
        "name": "Health / Energy",
        "items": [
            "Functional doctors",
            "Wellness specialists",
            "Somatic therapists",
            "Nutrition coaches"
        ]
    },
    "performance": {
        "name": "Performance",
        "items": [
            "Performance coaches",
            "Focus & time coaches",
            "Burnout specialists",
            "Habit designers"
        ]
    },
    "art_creative": {
        "name": "Art & Creative Industry",
        "items": [
            "Art managers and curators",
            "Gallerists",
            "Art dealers",
            "Professional photographers / videographers",
            "Sound producers",
            "High-level designers (fashion / graphic / UX)"
        ]
    },
    "business_startups": {
        "name": "Business & Startups",
        "items": [
            "Marketing strategists",
            "Bloggers / digital personalities producers",
            "SMM managers",
            "SEO / Ads US\u2013Europe",
            "Online course launch consultants",
            "Sales and funnel specialists",
            "Business coaches"
        ]
    },
    "personal_brand": {
        "name": "Personal Brand & PR",
        "items": [
            "PR agents (Europe / US / Asia)",
            "Media strategy specialists",
            "Brand strategists",
            "Content creators",
            "Community builders"
        ]
    },
    "lifestyle_travel": {
        "name": "Lifestyle & Travel",
        "items": [
            "Concierge services",
            "Luxury travel agents",
            "Relocation specialists",
            "Travel designers",
            "Retreat & event hosts"
        ]
    },
    "real_estate_spec": {
        "name": "Real Estate / Living",
        "items": [
            "Agents for rent/purchase worldwide",
            "Real estate investment specialists (yield-analysis)",
            "Property management specialists",
            "Property managers",
            "Interior stylists"
        ]
    },
    "community": {
        "name": "Community",
        "items": [
            "Community facilitators",
            "Networking hosts"
        ]
    }
}'''

new_specialists = '''SPECIALIST_CATEGORIES = {
    "legal_finance": {
        "name": "Legalization & Finance",
        "items": [
            "Tax specialist",
            "US visas",
            "European residence permits",
            "Schengen visas",
            "Citizenship",
            "Business legalization abroad",
            "Legal services",
            "Real estate investments",
            "Investments for HNWIs",
            "Wealth management"
        ]
    },
    "health_body": {
        "name": "Health & Body",
        "items": [
            "Doctors and health specialists",
            "Body-performance specialists",
            "Psychologists, mental health coaches",
            "Functional medicine experts",
            "Longevity & preventive health",
            "Osteopaths / chiropractors",
            "Sports recovery therapists",
            "Clinical nutritionists",
            "Mobility & posture specialists",
            "Medical diagnostics experts"
        ]
    },
    "wellbeing": {
        "name": "Wellbeing",
        "items": [
            "Wellness specialists",
            "Somatic therapists",
            "Nutrition coaches",
            "Senior psychologists",
            "Somatic therapy experts",
            "Sleep optimization pros",
            "Nervous system experts",
            "Recovery & regeneration",
            "Stress resilience experts"
        ]
    },
    "human_potential": {
        "name": "Human potential",
        "items": [
            "Performance coaches",
            "Focus & time coaches",
            "Burnout specialists",
            "Habit designers",
            "Burnout recovery specialists",
            "Life transition coaches",
            "Purpose & direction mentors",
            "Decision-making advisors",
            "Personal strategy consultants",
            "Resilience coaches",
            "Flow state facilitators",
            "Founder psychology advisors",
            "Identity shift mentors"
        ]
    },
    "art_creative": {
        "name": "Art & Creative Industry",
        "items": [
            "Art managers and curators",
            "Gallerists",
            "Art dealers",
            "Professional photographers / videographers",
            "Sound producers",
            "High-level designers (fashion / graphic / UX)",
            "Art fair insiders",
            "Collectors",
            "Collection advisors",
            "Cultural institution leaders",
            "Residency program directors",
            "Art investment consultants",
            "Music supervisors",
            "Independent label founders",
            "Festival programmers",
            "Talent bookers",
            "Cultural network connectors"
        ]
    },
    "business_startups": {
        "name": "Business & Startups",
        "items": [
            "Marketing strategists",
            "Bloggers / digital personalities producers",
            "SMM managers",
            "SEO / Ads US\\u2013Europe",
            "Online course launch consultants",
            "Sales and funnel specialists",
            "Business coaches",
            "Venture capital connectors",
            "Market entry strategists",
            "Cross-border expansion experts",
            "Investor relations advisors",
            "Capital raise strategists",
            "Startup ecosystem navigators",
            "Government relations advisors",
            "Licensing & compliance advisors",
            "Business model architects",
            "B2B growth strategists",
            "Distribution channel builders"
        ]
    },
    "personal_brand": {
        "name": "Personal Brand & PR",
        "items": [
            "PR agents (Europe / US / Asia)",
            "Media strategy specialists",
            "Brand strategists",
            "Content creators",
            "Community builders",
            "Executive presence coaches",
            "Media placement consultants",
            "Influence partnership advisors",
            "Podcast booking strategists",
            "Editorial strategy advisors",
            "Digital reputation architects",
            "High-profile networking advisors",
            "Awards & recognition strategists"
        ]
    },
    "lifestyle_travel": {
        "name": "Lifestyle & Travel",
        "items": [
            "Concierge services",
            "Luxury travel agents",
            "Relocation specialists",
            "Travel designers",
            "Retreat & event hosts",
            "Residency & visa strategists",
            "Property search consultants",
            "Second-home setup advisors",
            "Family relocation planners",
            "Experiential travel curators",
            "On-ground fixers (local experts)"
        ]
    },
    "real_estate_spec": {
        "name": "Real Estate",
        "items": [
            "Agents for rent/purchase worldwide",
            "Real estate investment specialists (yield-analysis)",
            "Property management specialists",
            "Property managers",
            "Off-market property brokers",
            "Real estate legal advisors",
            "Private market deal sourcers"
        ]
    },
    "complex_problem_solvers": {
        "name": "Complex Problem Solvers",
        "items": [
            "Special situations advisors",
            "Negotiation specialists",
            "Crisis navigation experts",
            "Behind-the-scenes fixers",
            "Cross-border problem solvers",
            "Access & escalation connectors"
        ]
    }
}'''

content = content.replace(old_specialists, new_specialists)

f.write_text(content, encoding='utf-8')
print("OK: form_data.py updated")

# ============================================================
# 2. UPDATE resources.py — Bug fixes
# ============================================================
f = bot_dir / 'handlers' / 'resources.py'
content = f.read_text(encoding='utf-8')

# Fix extra_keys - remove references to deleted fields, add art_link
content = content.replace(
    '"extra_keys": ["selected_offer_formats", "selected_interaction_formats", "selected_result_types"]',
    '"extra_keys": ["selected_offer_formats", "selected_result_types"]'
)
content = content.replace(
    '"extra_keys": ["selected_intro_formats"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["property_usage", "property_duration", "property_capacity"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["car_usage", "car_duration", "car_passengers"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["selected_equipment_access", "equipment_duration"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["aircraft_usage"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["vessel_usage"]',
    '"extra_keys": []'
)
content = content.replace(
    '"extra_keys": ["art_author", "art_author_name"]',
    '"extra_keys": ["art_author_name", "art_link"]'
)

# Fix "+N more" — show all items instead of truncating to 5
content = content.replace(
    '            items_str = ", ".join(res[\'items\'][:5])  # Limit to 5 items\r\n'
    '            if len(res[\'items\']) > 5:\r\n'
    '                items_str += f" (+{len(res[\'items\']) - 5} more)"\r\n',
    '            items_str = ", ".join(res[\'items\'])\r\n'
)

# Also add "Specialists" to get_resource_categories_keyboard if missing
# Actually the category keyboard already has "Specialists" via its category names

f.write_text(content, encoding='utf-8')
print("OK: resources.py updated")

# ============================================================
# 3. UPDATE keyboards.py — Art & Creative Works label
# ============================================================
f = bot_dir / 'keyboards.py'
content = f.read_text(encoding='utf-8')

# Fix artwork label
content = content.replace(
    '("🫧 Works of Art", "Artworks")',
    '("🫧 Art & Creative Works", "Artworks")'
)

# Add Specialists to category keyboard if missing
if '"Specialists"' not in content or '👨‍💼 Specialists' not in content:
    # Check if Specialists is already in the categories list
    pass  # It's not in the list, need to add

# Looking at the keyboard code, categories list doesn't include Specialists
# Let's add it
if '"Specialists"' not in content.split('get_resource_categories_keyboard')[1].split('return')[0]:
    content = content.replace(
        '        ("🤝🏻 Personal Introduction", "Personal Introductions to Key People"),\r\n',
        '        ("🤝🏻 Personal Introduction", "Personal Introductions to Key People"),\r\n'
        '        ("🩵 Specialists", "Specialists"),\r\n'
    )

f.write_text(content, encoding='utf-8')
print("OK: keyboards.py updated")

# ============================================================
# 4. UPDATE lots.py — Text-based lots form
# ============================================================
f = bot_dir / 'handlers' / 'lots.py'
content = f.read_text(encoding='utf-8')

# Replace the start_add_lot_flow function to use text-based template
old_start_flow = '''async def start_add_lot_flow(callback: CallbackQuery, state: FSMContext, lot_type: str):
    """Start the add lot flow"""
    await state.update_data(lot_type=lot_type)

    if lot_type == "share":
        text = (
            "Here you can share a resource you have available right now — a skill, service, access, or any other support you're ready to offer at this moment.\\n"
            "Describe your resource according to the short form below and send it to the chat. Your resource will appear in the list of active offers, and once it's used, you'll receive a point.\\n\\n"
            "First, select a **Category**:"
        )
    else:
        text = (
            "Here you can post a request for a resource, support, skill, or access you're currently looking for.\\n"
            "Describe what you need, where, and how soon. Your request will appear in the list of active requests so other members can respond or help.\\n\\n"
            "First, select a **Category**:"
        )

    # Use unique prefix to avoid conflict with Resources section
    await callback.message.edit_text(
        text,
        reply_markup=get_resource_categories_keyboard(prefix="lot_cat")
    )
    await state.set_state(AddLot.category)
    await callback.answer()'''

new_start_flow = '''async def start_add_lot_flow(callback: CallbackQuery, state: FSMContext, lot_type: str):
    """Start the add lot flow — text-based template"""
    await state.update_data(lot_type=lot_type)
    await callback.message.delete()

    if lot_type == "share":
        text = (
            "Here you can describe a resource you want to share RIGHT NOW to receive "
            "1 point in exchange \\u2014 a skill, service, access, or any other support "
            "you\\u2019re ready to offer\\n\\n"
            "Describe your resource according to the short form below (IT\\u2019S IMPORTANT) "
            "and send it to the chat. Your resource will appear in the list of active offers, "
            "and once it\\u2019s used, you\\u2019ll receive a point.\\n\\n"
            "Copy this text and fill in the information following the example in brackets \\U0001f447\\U0001f3fb\\n\\n"
            "Type of Resource:\\n"
            "(e.g. consultation, introduction, equipment, access, skill, space)\\n"
            "Description:\\n"
            "(briefly describe what exactly you\\u2019re offering and in what form)\\n"
            "Location:\\n"
            "(city or online)\\n"
            "Availability:\\n"
            "(specific dates, this week, next 14 days, flexible)\\n\\n"
            "EXAMPLE:\\n\\n"
            "Type of Resource: english lessons\\n"
            "Description: 60 minutes 4 times per month\\n"
            "Location: Online\\n"
            "Availability: Only this month"
        )
    else:
        text = (
            "Here you can post a request for a resource, support, skill, or access "
            "you\\u2019re currently looking for.\\n"
            "Describe what you need, where, and how soon. Your request will appear "
            "in the list of active requests so other members can respond or help.\\n\\n"
            "Copy this text and fill in the information following the example in brackets \\U0001f447\\U0001f3fb\\n\\n"
            "Type of Resource:\\n"
            "(e.g. consultation, introduction, equipment, access, skill, space)\\n"
            "Description:\\n"
            "(briefly describe what you\\u2019re looking for and in what form)\\n"
            "Location:\\n"
            "(city or online)\\n"
            "When Needed:\\n"
            "(ASAP, specific dates, this week, next 14 days, flexible)\\n\\n"
            "EXAMPLE:\\n"
            "Type of Resource: Apartment\\n"
            "Description: Looking for a place to stay in Bangkok\\n"
            "Location: Bangkok\\n"
            "When Needed: 13-17.02"
        )

    await callback.message.answer(text, reply_markup=get_cancel_keyboard())
    await state.set_state(AddLot.description)
    await callback.answer()'''

content = content.replace(old_start_flow, new_start_flow)

# Replace process_lot_description to parse the template text and save directly
old_process_desc = '''@router.message(AddLot.description, F.text)
async def process_lot_description(message: Message, state: FSMContext):
    if message.text.strip() == "🔙 Back":
        await message.answer("Type of Resource:", reply_markup=get_cancel_keyboard())
        await state.set_state(AddLot.type_text)
        return

    await state.update_data(description=message.text)

    # Remove previous Reply keyboard before showing Inline city selection
    await message.answer("Select Location:", reply_markup=ReplyKeyboardRemove())

    # Send city selection keyboard with prefix "lot_city"
    await message.answer(
        "Location\\ncity or online",
        reply_markup=get_cities_keyboard(prefix="lot_city")
    )
    await state.set_state(AddLot.location)'''

new_process_desc = '''@router.message(AddLot.description, F.text)
async def process_lot_description(message: Message, state: FSMContext, db: Database):
    if message.text.strip() == "\\U0001f519 Back":
        # Go back to lots menu
        await message.answer(
            "\\U0001f499Lots\\n\\n"
            "Here you can manage what you share and what you\\u2019re looking for.\\n\\n"
            "Select an option:",
            reply_markup=get_lots_type_keyboard()
        )
        await state.clear()
        return

    # Parse the template text
    text = message.text.strip()
    data = await state.get_data()
    lot_type = data.get("lot_type", "share")

    # Try to extract fields from the template
    import re as _re
    type_match = _re.search(r"Type of Resource[:\\s]*(.+?)(?:\\n|$)", text, _re.IGNORECASE)
    desc_match = _re.search(r"Description[:\\s]*(.+?)(?:\\n|$)", text, _re.IGNORECASE)
    loc_match = _re.search(r"Location[:\\s]*(.+?)(?:\\n|$)", text, _re.IGNORECASE)
    avail_key = "Availability" if lot_type == "share" else "When Needed"
    avail_match = _re.search(rf"{avail_key}[:\\s]*(.+?)(?:\\n|$)", text, _re.IGNORECASE)

    title = type_match.group(1).strip() if type_match else text[:100]
    description = desc_match.group(1).strip() if desc_match else text
    location = loc_match.group(1).strip() if loc_match else ""
    availability = avail_match.group(1).strip() if avail_match else ""

    # Save lot
    lot_id = await db.add_lot(
        user_id=message.from_user.id,
        lot_type=lot_type,
        title=title,
        description=description,
        category="",
        location_text=location,
        availability=availability,
        status="approved"
    )

    await state.clear()

    if lot_id:
        type_emoji = "\\U0001f381" if lot_type == "share" else "\\U0001f50d"
        await message.answer(
            f"\\u2705 Your lot has been published!\\n\\n"
            f"{type_emoji} **{title}**\\n"
            f"It\\u2019s now visible to other community members.",
            reply_markup=get_menu_keyboard(message.from_user.id)
        )
        await message.answer(
            "\\U0001f499Lots\\n\\n"
            "Here you can manage what you share and what you\\u2019re looking for.\\n\\n"
            "Select an option:",
            reply_markup=get_lots_type_keyboard()
        )
    else:
        await message.answer(
            "\\u274c Failed to add lot. Please try again.",
            reply_markup=get_menu_keyboard(message.from_user.id)
        )'''

content = content.replace(old_process_desc, new_process_desc)

# Add get_lots_type_keyboard and get_menu_keyboard imports if not present
if 'get_lots_type_keyboard' not in content.split('from bot.keyboards import')[1].split(')')[0]:
    pass  # Already imported

f.write_text(content, encoding='utf-8')
print("OK: lots.py updated")

print("\n=== ALL DATA FILES UPDATED ===")
