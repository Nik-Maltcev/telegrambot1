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

# "Resources" flow: Categories -> List Lots (Share type)
# We assume "Resources" displays active offers (Lots of type 'share') organized by category.

@router.message(F.text == "🪩Resources")
async def show_resources_menu(message: Message, db: Database):
    """Show resources section - List Categories"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    # Direct to categories
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
        "Real Estate": "🗽 Real Estate\n\nProperties, apartments, houses, and real estate opportunities available for exchange or temporary use.",
        "Cars and Other Vehicles": "🖤 Cars\n\nVehicles available for sharing, rent, or exchange within the community.",
        "Air Transport": "🛩️ Aircrafts\n\nPrivate jets, helicopters, and aircraft available for community members.",
        "Water Transport / Vessels": "💎 Boats\n\nYachts, boats, and watercraft available for exchange or use.",
        "Equipment": "🎧 Equipment\n\nTools, machinery, and equipment available for sharing.",
        "Skills and Knowledge": "🧑🏼‍💻 Skills and Knowledge\n\nExpertise, mentoring, and educational resources offered by members.",
        "Unique opportunities": "🫆 Unique Opportunities\n\nSpecial opportunities, access, and unique experiences.",
        "Artworks": "🫧 Works of Art\n\nArtwork, collectibles, and creative works available for viewing or exchange.",
        "Personal Introductions to Key People": "🤝🏻 Personal Introduction\n\nConnections and introductions to specific professional or social circles.",
        "Specialists": "👨‍💼 Specialists\n\nTrusted professionals and contacts recommended by members."
    }

    # Use description from dict or default
    description = category_descriptions.get(category, f"📦 {category}")

    # Fetch Lots of type 'share' and status 'approved' with this category
    # We added get_lots_by_category to db
    resources = await db.get_lots_by_category(category)

    await callback.message.edit_text(
        f"{description}\n\n"
        f"Loading resources...",
        reply_markup=None # Remove keyboard momentarily
    )

    if not resources:
        await callback.message.edit_text(
            f"{description}\n\n"
            f"No resources found in this category yet.",
            reply_markup=get_back_keyboard("back_to_resources")
        )
        await callback.answer()
        return

    # Display resources
    resources_text = f"{description}\n\n"

    for res in resources:
        telegram_username = f"(@{res['username']})" if res['username'] else ""
        location = f"📍 {res['location_text']}\n" if res['location_text'] else ""
        avail = f"📅 Availability: {res['availability']}\n" if res['availability'] else ""

        resources_text += (
            f"━━━━━━━━━━━━━━━\n"
            f"📌 {res['title']}\n"
            f"{location}"
            f"📝 {res['description']}\n"
            f"{avail}"
            f"👤 Owner: {res['name']} {telegram_username}\n\n"
        )

    if len(resources_text) > 4096:
        # Split
        chunks = [resources_text[i:i+4096] for i in range(0, len(resources_text), 4096)]
        await callback.message.edit_text(chunks[0])
        for chunk in chunks[1:]:
            await callback.message.answer(chunk)

        await callback.message.answer(
            "End of list",
            reply_markup=get_back_keyboard("back_to_resources")
        )
    else:
        await callback.message.edit_text(
            resources_text,
            reply_markup=get_back_keyboard("back_to_resources")
        )

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

# Legacy callbacks (res_city, etc.) might need cleanup or ignored if we switched flow completely.
# I'm replacing the file content so old handlers are gone.
