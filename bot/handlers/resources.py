from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import (
    get_cities_select_keyboard,
    get_resource_categories_keyboard,
    get_resource_card_keyboard,
    get_back_keyboard
)
from bot.form_data import CITIES

router = Router()

# Store user's selected cities in memory
# format: {user_id: {"cities": set(selected_cities)}}
user_resource_selection = {}


@router.message(F.text == "📦 Resources")
async def show_resources_menu(message: Message, db: Database):
    """Show resources section - select city first"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    # Initialize selection
    user_resource_selection[message.from_user.id] = {"cities": set()}

    await message.answer(
        "📦 Resources\n\n"
        "First, select cities to filter resources (you can select multiple):",
        reply_markup=get_cities_select_keyboard("res_city", "res_city_done", set())
    )


@router.callback_query(F.data.startswith("res_city:"))
async def toggle_resource_city(callback: CallbackQuery):
    """Toggle city selection"""
    import hashlib

    # helper to find city by hash
    def find_city(h):
        for c in CITIES:
            if hashlib.md5(c.encode()).hexdigest()[:8] == h:
                return c
        return None

    city_hash = callback.data.split(":", 1)[1]
    city = find_city(city_hash)

    user_id = callback.from_user.id
    if user_id not in user_resource_selection:
        user_resource_selection[user_id] = {"cities": set()}

    if city:
        current_cities = user_resource_selection[user_id]["cities"]
        if city in current_cities:
            current_cities.remove(city)
        else:
            current_cities.add(city)

        await callback.message.edit_reply_markup(
            reply_markup=get_cities_select_keyboard("res_city", "res_city_done", current_cities)
        )

    await callback.answer()


@router.callback_query(F.data == "res_city_done")
async def show_resource_categories(callback: CallbackQuery):
    """Show resource categories after city selection"""
    user_id = callback.from_user.id
    if user_id not in user_resource_selection or not user_resource_selection[user_id]["cities"]:
        await callback.answer("Please select at least one city.", show_alert=True)
        return

    cities = list(user_resource_selection[user_id]["cities"])
    cities_str = ", ".join(cities)
    if len(cities) > 3:
        cities_str = f"{len(cities)} cities selected"

    await callback.message.edit_text(
        f"📦 Resources in: {cities_str}\n\n"
        f"Select a category:",
        reply_markup=get_resource_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("res_cat:"))
async def show_resources_in_category(callback: CallbackQuery, db: Database):
    """Show resources in selected category"""
    category = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id

    if user_id not in user_resource_selection or not user_resource_selection[user_id]["cities"]:
        await callback.answer("Please select a city first", show_alert=True)
        return

    cities = list(user_resource_selection[user_id]["cities"])

    # Fetch resources for all selected cities
    # Note: DB method might need update to handle multiple cities, or we loop
    # For now, let's assume we iterate or if DB supports list.
    # checking db.py... get_resources_by_city_and_category(city, category)
    # I'll just fetch for each city and aggregate.

    all_resources = []
    for city in cities:
        res = await db.get_resources_by_city_and_category(city, category)
        if res:
            all_resources.extend(res)

    # Show category description
    category_descriptions = {
        "Real Estate": "🏠 Real Estate\n\nProperties, apartments, houses, and real estate opportunities available for exchange or temporary use.",
        "Cars": "🚗 Cars\n\nVehicles available for sharing, rent, or exchange within the community.",
        "Aircrafts": "✈️ Aircrafts\n\nPrivate jets, helicopters, and aircraft available for community members.",
        "Boats": "⛵ Boats\n\nYachts, boats, and watercraft available for exchange or use.",
        "Equipment": "🔧 Equipment\n\nTools, machinery, and equipment available for sharing.",
        "Skills and Knowledge": "🎓 Skills and Knowledge\n\nExpertise, mentoring, and educational resources offered by members.",
        "Unique Opportunities": "✨ Unique Opportunities\n\nSpecial opportunities, access, and unique experiences.",
        "Works of Art": "🎨 Works of Art\n\nArtwork, collectibles, and creative works available for viewing or exchange.",
        "Personal Introduction to Specific Circles": "🤝 Personal Introduction\n\nConnections and introductions to specific professional or social circles."
    }

    description = category_descriptions.get(category, f"📦 {category}")
    await callback.message.answer(f"ℹ️ About this section and how it works:\n\nThis section allows you to find and request resources from other community members. You can browse by category and city, and contact the owner directly to arrange an exchange.\n\n{description}")

    if not all_resources:
        await callback.answer(
            f"No resources found in {category}",
            show_alert=True
        )
        return

    for res in all_resources:
        telegram_username = f"(@{res['username']})" if res['username'] else ""
        instagram_info = f" | 📸 @{res['instagram']}" if res['instagram'] else ""
        resource_text = (
            f"📌 {res['title']}\n"
            f"📍 {res['city']}\n"
            f"📝 {res['description']}\n\n"
            f"👤 Owner: {res['name']} {telegram_username} (💰 {res['points']} points){instagram_info}\n\n"
        )
        await callback.message.answer(
            resource_text,
            reply_markup=get_resource_card_keyboard(res['user_id'], res['instagram'])
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_resources")
async def back_to_resources(callback: CallbackQuery):
    """Go back to city selection for resources"""
    user_id = callback.from_user.id
    selected = set()
    if user_id in user_resource_selection:
        selected = user_resource_selection[user_id]["cities"]

    await callback.message.edit_text(
        "📦 Resources\n\n"
        "Select cities to filter resources:",
        reply_markup=get_cities_select_keyboard("res_city", "res_city_done", selected)
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_category")
async def back_to_category(callback: CallbackQuery):
    """Go back to category selection"""
    user_id = callback.from_user.id
    cities_str = "Selected cities"
    if user_id in user_resource_selection:
        cities = list(user_resource_selection[user_id]["cities"])
        cities_str = ", ".join(cities)
        if len(cities) > 3:
            cities_str = f"{len(cities)} cities selected"

    await callback.message.edit_text(
        f"📦 Resources in: {cities_str}\n\n"
        f"Select a category:",
        reply_markup=get_resource_categories_keyboard()
    )
    await callback.answer()
