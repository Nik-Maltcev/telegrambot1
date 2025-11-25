from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from bot.database import Database
from bot.keyboards import (
    get_admin_panel_keyboard,
    get_confirmation_keyboard,
    get_cancel_keyboard,
    get_admin_menu_keyboard
)
from bot.config import ADMIN_IDS

router = Router()


class ManagePoints(StatesGroup):
    user_id = State()
    points = State()


class AddOpenResource(StatesGroup):
    section = State()
    title = State()
    description = State()
    link = State()
    city = State()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


@router.message(F.text == "⚙️ Admin Panel")
async def show_admin_panel(message: Message):
    """Show admin panel (only for admins)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ You don't have access to this section.")
        return

    await message.answer(
        "⚙️ Admin Panel\n\n"
        "Manage community resources and users.\n\n"
        "Select an option:",
        reply_markup=get_admin_panel_keyboard()
    )


@router.callback_query(F.data == "admin:users")
async def manage_users(callback: CallbackQuery, db: Database):
    """Show all users"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    users = await db.get_all_users()

    if not users:
        await callback.answer("No users found", show_alert=True)
        return

    users_text = "👥 All Users\n\n"

    for user in users:
        users_text += (
            f"━━━━━━━━━━━━━━━\n"
            f"👤 {user['name']}\n"
            f"ID: {user['user_id']}\n"
            f"Username: @{user['username'] if user['username'] else 'none'}\n"
            f"Main City: {user['main_city']}\n"
            f"Current City: {user['current_city']}\n"
            f"Instagram: {user['instagram'] if user['instagram'] else 'none'}\n"
            f"💰 Points: {user['points']}\n"
            f"Registered: {user['registered_at'][:10]}\n\n"
        )

    # Split if message is too long
    if len(users_text) > 4096:
        chunks = [users_text[i:i+4096] for i in range(0, len(users_text), 4096)]
        await callback.message.answer(chunks[0])
        for chunk in chunks[1:]:
            await callback.message.answer(chunk)
    else:
        await callback.message.answer(users_text)

    await callback.answer()


@router.callback_query(F.data == "admin:points")
async def start_manage_points(callback: CallbackQuery, state: FSMContext):
    """Start points management"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    await callback.message.answer(
        "💰 Manage Points\n\n"
        "Enter the user ID whose points you want to change:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(ManagePoints.user_id)
    await callback.answer()


@router.message(ManagePoints.user_id, F.text)
async def process_user_id_for_points(message: Message, state: FSMContext, db: Database):
    """Process user ID for points management"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    try:
        user_id = int(message.text)
        user = await db.get_user(user_id)

        if not user:
            await message.answer("❌ User not found. Please try again or cancel.")
            return

        await state.update_data(user_id=user_id)
        await message.answer(
            f"User: {user['name']}\n"
            f"Current points: {user['points']}\n\n"
            f"Enter new points value:",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(ManagePoints.points)

    except ValueError:
        await message.answer("❌ Invalid user ID. Please enter a number.")


@router.message(ManagePoints.points, F.text)
async def process_points_value(message: Message, state: FSMContext, db: Database):
    """Process new points value"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    try:
        points = int(message.text)
        data = await state.get_data()
        user_id = data['user_id']

        success = await db.update_user_points(user_id, points)

        await state.clear()

        if success:
            user = await db.get_user(user_id)
            await message.answer(
                f"✅ Points updated successfully!\n\n"
                f"User: {user['name']}\n"
                f"New points: {points}"
            )
        else:
            await message.answer("❌ Failed to update points.")

    except ValueError:
        await message.answer("❌ Invalid points value. Please enter a number.")


@router.callback_query(F.data == "admin:open_resources")
async def start_add_open_resource(callback: CallbackQuery, state: FSMContext):
    """Start adding open resource"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    await callback.message.answer(
        "➕ Add Open Resource\n\n"
        "Enter section type (maps/accesses/specialists):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddOpenResource.section)
    await callback.answer()


@router.message(AddOpenResource.section, F.text)
async def process_section(message: Message, state: FSMContext):
    """Process section for open resource"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    if message.text.lower() not in ["maps", "accesses", "specialists"]:
        await message.answer("❌ Invalid section. Use: maps, accesses, or specialists")
        return

    await state.update_data(section=message.text.lower())
    await message.answer(
        "Enter title:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddOpenResource.title)


@router.message(AddOpenResource.title, F.text)
async def process_title(message: Message, state: FSMContext):
    """Process title for open resource"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    await state.update_data(title=message.text)
    await message.answer(
        "Enter description:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddOpenResource.description)


@router.message(AddOpenResource.description, F.text)
async def process_description(message: Message, state: FSMContext):
    """Process description for open resource"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    await state.update_data(description=message.text)
    await message.answer(
        "Enter link (or '-' if none):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddOpenResource.link)


@router.message(AddOpenResource.link, F.text)
async def process_link(message: Message, state: FSMContext):
    """Process link for open resource"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    link = message.text if message.text != "-" else ""
    await state.update_data(link=link)
    await message.answer(
        "Enter city (or '-' if not applicable):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddOpenResource.city)


@router.message(AddOpenResource.city, F.text)
async def process_city(message: Message, state: FSMContext, db: Database):
    """Process city and complete adding open resource"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Returned to menu.", reply_markup=get_admin_menu_keyboard())
        return

    city = message.text if message.text != "-" else ""
    data = await state.get_data()

    success = await db.add_open_resource(
        section=data['section'],
        title=data['title'],
        description=data['description'],
        link=data['link'],
        city=city
    )

    await state.clear()

    if success:
        await message.answer(
            f"✅ Open resource added successfully!\n\n"
            f"Section: {data['section']}\n"
            f"Title: {data['title']}"
        )
    else:
        await message.answer("❌ Failed to add open resource.")


@router.callback_query(F.data == "admin:resources")
async def manage_resources(callback: CallbackQuery):
    """Manage resources (placeholder)"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    await callback.message.answer(
        "📦 Manage Resources\n\n"
        "This feature allows you to moderate and manage user-submitted resources.\n"
        "Coming soon..."
    )
    await callback.answer()


def generate_invite_token(length=16):
    """Generate a random invite token."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


@router.callback_query(F.data == "admin:generate_token")
async def generate_token(callback: CallbackQuery, db: Database):
    """Generate and show a new invite token."""
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    token = generate_invite_token()
    success = await db.add_invite_token(token)

    if success:
        await callback.message.answer(
            f"🔑 New Invite Token\n\n"
            f"Here is the new single-use invite token:\n\n"
            f"`{token}`\n\n"
            f"Share it with a new user to allow them to register."
        )
    else:
        await callback.message.answer("❌ Failed to generate a new token.")

    await callback.answer()
