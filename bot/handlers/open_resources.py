from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import get_open_resources_keyboard, get_back_keyboard

router = Router()


@router.message(F.text == "🗂 Open Resources Database")
async def show_open_resources_menu(message: Message, db: Database):
    """Show open resources database menu"""
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ You are not registered. Please use /start to register.")
        return

    await message.answer(
        "🗂 Open Resources Database\n\n"
        "Access shared maps, links, and verified specialists.\n\n"
        "Select a section:",
        reply_markup=get_open_resources_keyboard()
    )


@router.callback_query(F.data.startswith("open:"))
async def show_open_resources_section(callback: CallbackQuery, db: Database):
    """Show open resources in selected section"""
    section = callback.data.split(":", 1)[1]

    resources = await db.get_open_resources(section)

    section_info = {
        "maps": ("🗺 Google Maps", "City maps and location guides"),
        "accesses": ("🔑 Access Links", "Shared access to platforms and services"),
        "specialists": ("👨‍💼 Verified Specialists", "Trusted professionals and contacts")
    }

    emoji, description = section_info.get(section, ("📂", "Resources"))

    if not resources:
        await callback.message.edit_text(
            f"{emoji}\n\n"
            f"{description}\n\n"
            f"No resources available in this section yet.",
            reply_markup=get_back_keyboard("back_to_open_resources")
        )
        await callback.answer()
        return

    resources_text = f"{emoji}\n\n{description}\n\n"

    for res in resources:
        city_info = f"📍 {res['city']}\n" if res['city'] else ""
        link_info = f"🔗 {res['link']}\n" if res['link'] else ""

        resources_text += (
            f"━━━━━━━━━━━━━━━\n"
            f"📌 {res['title']}\n"
            f"{city_info}"
            f"📝 {res['description']}\n"
            f"{link_info}\n"
        )

    # Split if message is too long
    if len(resources_text) > 4096:
        chunks = [resources_text[i:i+4096] for i in range(0, len(resources_text), 4096)]
        await callback.message.edit_text(chunks[0])
        for chunk in chunks[1:]:
            await callback.message.answer(chunk)
    else:
        await callback.message.edit_text(
            resources_text,
            reply_markup=get_back_keyboard("back_to_open_resources")
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_open_resources")
async def back_to_open_resources(callback: CallbackQuery):
    """Go back to open resources menu"""
    await callback.message.edit_text(
        "🗂 Open Resources Database\n\n"
        "Access shared maps, links, and verified specialists.\n\n"
        "Select a section:",
        reply_markup=get_open_resources_keyboard()
    )
    await callback.answer()
