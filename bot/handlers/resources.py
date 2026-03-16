from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import (
    get_resource_categories_keyboard,
    get_back_keyboard
)
import json

router = Router()

# Mapping from category to questionnaire data keys
CATEGORY_DATA_MAPPING = {
    "Skills and Knowledge": {
        "items_key": "selected_skill_items",
        "cities_key": None,  # Skills are not location-specific in questionnaire
        "extra_keys": ["selected_offer_formats", "selected_result_types"]
    },
    "Personal Introductions to Key People": {
        "items_key": "selected_intro_items",
        "cities_key": "selected_intro_cities",
        "extra_keys": []
    },
    "Real Estate": {
        "items_key": "selected_property_types",
        "cities_key": "selected_prop_cities",
        "extra_keys": []
    },
    "Cars and Other Vehicles": {
        "items_key": "car_info",  # Single value
        "cities_key": "selected_car_cities",
        "extra_keys": []
    },
    "Equipment": {
        "items_key": "selected_equipment_types",
        "cities_key": "selected_equip_cities",
        "extra_keys": []
    },
    "Air Transport": {
        "items_key": "selected_aircraft_types",
        "cities_key": "selected_air_cities",
        "extra_keys": []
    },
    "Water Transport / Vessels": {
        "items_key": "selected_vessel_types",
        "cities_key": "selected_vessel_cities",
        "extra_keys": []
    },
    "Specialists": {
        "items_key": "specialists_list",
        "cities_key": None,
        "extra_keys": []
    },
    "Artworks": {
        "items_key": "art_form",
        "cities_key": "art_location",
        "extra_keys": ["art_author_name", "art_link"]
    }
}


def extract_resources_from_registration(reg_data: dict, category: str, user_info: dict) -> list:
    """Extract resources for a specific category from registration data."""
    resources = []
    mapping = CATEGORY_DATA_MAPPING.get(category)
    
    if not mapping:
        return resources
    
    items_key = mapping["items_key"]
    cities_key = mapping["cities_key"]
    extra_keys = mapping["extra_keys"]
    
    # Get items
    items = reg_data.get(items_key, [])
    if not items:
        return resources
    
    # Handle single value vs list
    if isinstance(items, str):
        items = [items]
    
    # Format Specialist dictionaries if we are in the Specialists category
    if category == "Specialists":
        formatted_items = []
        for spec in items:
            if isinstance(spec, dict):
                spec_name = spec.get("name", "Unknown")
                spec_cat = spec.get("category", "")
                spec_contact = spec.get("contact", "")
                spec_ref = spec.get("referral", "")
                spec_conn = spec.get("connection", "")
                
                info = f"{spec_name}"
                if spec_cat: info += f" ({spec_cat})"
                if spec_contact: info += f" - Contact: {spec_contact}"
                if spec_ref: info += f" - Ref: {spec_ref}"
                formatted_items.append(info)
            else:
                formatted_items.append(str(spec))
        items = formatted_items
    
    # Get cities
    cities = []
    if cities_key:
        cities = reg_data.get(cities_key, [])
        if isinstance(cities, str):
            cities = [cities]
    
    # Get extra info
    extra_info = []
    for key in extra_keys:
        value = reg_data.get(key)
        if value:
            # specifically check for art link to format it nicely
            if key == "art_link":
                extra_info.append(f"🔗 Link: {value}")
            elif key == "art_author_name":
                extra_info.append(f"✍️ Author: {value}")
            elif isinstance(value, list):
                extra_info.extend(value)
            else:
                extra_info.append(str(value))
    
    # Build resource entry
    resource = {
        "user_id": user_info["user_id"],
        "name": user_info["name"],
        "username": user_info.get("username"),
        "instagram": user_info.get("instagram"),
        "points": user_info.get("points", 0),
        "items": items,
        "cities": cities if cities else [user_info.get("main_city", "")],
        "extra": extra_info
    }
    
    resources.append(resource)
    return resources


@router.message(F.text == "🪩Resources")
async def show_resources_menu(message: Message, db: Database):
    """Show resources section - List Categories"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "🪩Resources\n\n"
        "Select a category to browse resources:",
        reply_markup=get_resource_categories_keyboard()
    )


@router.callback_query(F.data.startswith("res_cat:"))
async def show_resources_in_category(callback: CallbackQuery, db: Database):
    """Show resources in selected category"""
    category = callback.data.split(":", 1)[1]

    # Category Descriptions
    category_descriptions = {
        "Real Estate": "🗽 Real Estate\n\nProperties available for exchange or temporary use.",
        "Cars and Other Vehicles": "🖤 Cars\n\nVehicles available for sharing within the community.",
        "Air Transport": "🛩️ Aircrafts\n\nPrivate jets, helicopters, and aircraft available.",
        "Water Transport / Vessels": "💎 Boats\n\nYachts, boats, and watercraft available.",
        "Equipment": "🎧 Equipment\n\nTools and equipment available for sharing.",
        "Skills and Knowledge": "🧑🏼‍💻 Skills and Knowledge\n\nExpertise and educational resources offered by members.",
        "Unique opportunities": "🫆 Unique Opportunities\n\nSpecial opportunities and unique experiences.",
        "Artworks": "🫧 Art & Creative Works\n\nArtwork and creative works available.",
        "Personal Introductions to Key People": "🤝🏻 Personal Introduction\n\nConnections to professional or social circles.",
        "Specialists": "👨‍💼 Specialists\n\nTrusted professionals recommended by members."
    }

    description = category_descriptions.get(category, f"📦 {category}")

    await callback.message.edit_text(f"{description}\n\nLoading resources...")

    # Get resources from Lots (manually added)
    lots_resources = await db.get_lots_by_category(category)
    
    # Get resources from registration questionnaires
    all_reg_data = await db.get_all_registration_data()
    questionnaire_resources = []
    
    for user_data in all_reg_data:
        try:
            reg_data = json.loads(user_data["answer_data"])
            user_info = {
                "user_id": user_data["user_id"],
                "name": user_data["name"],
                "username": user_data["username"],
                "instagram": user_data["instagram"],
                "points": user_data["points"],
                "main_city": user_data["main_city"]
            }
            extracted = extract_resources_from_registration(reg_data, category, user_info)
            questionnaire_resources.extend(extracted)
        except (json.JSONDecodeError, KeyError):
            continue

    # Build response text
    resources_text = f"{description}\n\n"
    has_resources = False

    # Show questionnaire resources
    if questionnaire_resources:
        has_resources = True
        for res in questionnaire_resources:
            telegram_link = f"@{res['username']}" if res['username'] else ""
            cities_str = ", ".join(res['cities']) if res['cities'] else "Not specified"
            
            # Format items as a bulleted list or comma-separated depending on length, show all
            if category == "Specialists":
                items_str = "\n  • ".join([""] + res['items']).lstrip()
            else:
                items_str = ", ".join(str(i) for i in res['items'])
            
            extra_str = ""
            if res['extra']:
                # Format each extra stat on a new line
                extra_str = "\n".join(res['extra']) + "\n"
            
            resources_text += (
                f"━━━━━━━━━━━━━━━\n"
                f"🐥 {res['name']} {telegram_link}\n"
                f"🪩 {cities_str}\n"
                f"✉️ {items_str}\n"
                f"{extra_str}"
                f"🩵 Points: {res['points']}\n\n"
            )

    # Show lots resources
    if lots_resources:
        has_resources = True
        if questionnaire_resources:
            resources_text += "━━━ Additional Lots ━━━\n\n"
        
        for res in lots_resources:
            telegram_username = f"(@{res['username']})" if res['username'] else ""
            location = f"📍 {res['location_text']}\n" if res['location_text'] else ""
            avail = f"📅 {res['availability']}\n" if res['availability'] else ""

            resources_text += (
                f"━━━━━━━━━━━━━━━\n"
                f"📌 {res['title']}\n"
                f"{location}"
                f"📝 {res['description']}\n"
                f"{avail}"
                f"👤 {res['name']} {telegram_username}\n\n"
            )

    if not has_resources:
        resources_text += "No resources found in this category yet."

    # Handle long messages
    if len(resources_text) > 4096:
        chunks = [resources_text[i:i+4096] for i in range(0, len(resources_text), 4096)]
        await callback.message.edit_text(chunks[0])
        for chunk in chunks[1:]:
            await callback.message.answer(chunk)
        await callback.message.answer("End of list", reply_markup=get_back_keyboard("back_to_resources"))
    else:
        await callback.message.edit_text(resources_text, reply_markup=get_back_keyboard("back_to_resources"))

    await callback.answer()


@router.callback_query(F.data == "back_to_resources")
async def back_to_resources_menu(callback: CallbackQuery):
    """Go back to categories"""
    await callback.message.edit_text(
        "🪩Resources\n\n"
        "Select a category to browse resources:",
        reply_markup=get_resource_categories_keyboard()
    )
    await callback.answer()
