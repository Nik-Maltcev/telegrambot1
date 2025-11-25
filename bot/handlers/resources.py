from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import (
    get_cities_keyboard,
    get_resource_categories_keyboard,
    get_resource_card_keyboard,
    get_back_keyboard
)

router = Router()

# Store user's selected city in memory (in production, use FSM or database)
user_resource_city = {}


@router.message(F.text == "📦 Resources")
async def show_resources_menu(message: Message, db: Database):
    """Show resources section - select city first"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "📦 Resources\n\n"
        "First, select a city to filter resources:",
        reply_markup=get_cities_keyboard()
    )


@router.callback_query(F.data.startswith("city:") & F.message.text.contains("Resources"))
async def show_resource_categories(callback: CallbackQuery, db: Database):
    """Show resource categories after city selection"""
    city = callback.data.split(":", 1)[1]
    user_resource_city[callback.from_user.id] = city

    await callback.message.edit_text(
        f"📦 Resources in {city}\n\n"
        f"Select a category:",
        reply_markup=get_resource_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("res_cat:"))
async def show_resources_in_category(callback: CallbackQuery, db: Database):
    """Show resources in selected category"""
    category = callback.data.split(":", 1)[1]
    city = user_resource_city.get(callback.from_user.id, "")

    if not city:
        await callback.answer("Please select a city first", show_alert=True)
        return

    resources = await db.get_resources_by_city_and_category(city, category)

    if not resources:
        await callback.answer(
            f"No resources found in {category} for {city}",
            show_alert=True
        )
        return

    # Show category description
    category_descriptions = {
        "Real Estate": "🏠 Real Estate\n\nProperties, apartments, houses, and real estate opportunities available for exchange or temporary use.",
        "Cars": "🚗 Cars\n\nVehicles available for sharing, rent, or exchange within the community.",
        "Aircrafts": "✈️ Aircrafts\n\nPrivate jets, helicopters, and aircraft available for community members.",
        "Boats": "⛵ Boats\n\nYachts, boats, and watercraft available for exchange or use.",
        "Equipment": "🔧 Equipment\n\nTools, machinery, and equipment available for sharing.",
        "Skills and Knowledge": "🎓 Skills and Knowledge\n\nExpertise, mentoring, and educational resources offered by members.",
        "Experience and Time": "⏰ Experience and Time\n\nTime, experience, and personal assistance offered by members.",
        "Unique Opportunities": "✨ Unique Opportunities\n\nSpecial opportunities, access, and unique experiences.",
        "Works of Art": "🎨 Works of Art\n\nArtwork, collectibles, and creative works available for viewing or exchange.",
        "Personal Introduction to Specific Circles": "🤝 Personal Introduction\n\nConnections and introductions to specific professional or social circles."
    }

    description = category_descriptions.get(category, f"📦 {category}")
    await callback.message.answer(f"ℹ️ About this section:\n\nThis section allows you to find and request resources from other community members. You can browse by category and city, and contact the owner directly to arrange an exchange.\n\n{description}")

    for res in resources:
        telegram_username = f"(@{res['username']})" if res['username'] else ""
        instagram_info = f" | 📸 @{res['instagram']}" if res['instagram'] else ""
        resource_text = (
            f"📌 {res['title']}\n"
            f"📝 {res['description']}\n\n"
            f"👤 Owner: {res['name']} {telegram_username} (💰 {res['points']} points){instagram_info}\n\n"
        )
        await callback.message.answer(
            resource_text,
            reply_markup=get_resource_card_keyboard(res['user_id'], res['instagram'])
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_resources")
async def back_to_resources(callback: CallbackQuery, db: Database):
    """Go back to city selection for resources"""
    await callback.message.edit_text(
        "📦 Resources\n\n"
        "Select a city to filter resources:",
        reply_markup=get_cities_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_category")
async def back_to_category(callback: CallbackQuery):
    """Go back to category selection"""
    city = user_resource_city.get(callback.from_user.id, "Unknown")

    await callback.message.edit_text(
        f"📦 Resources in {city}\n\n"
        f"Select a category:",
        reply_markup=get_resource_categories_keyboard()
    )
    await callback.answer()
