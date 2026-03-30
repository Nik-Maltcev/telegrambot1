import secrets
import string
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from bot.database import Database
from bot.keyboards import (
    get_admin_panel_keyboard,
    get_confirmation_keyboard,
    get_cancel_keyboard,
    get_menu_keyboard,
    get_lot_moderation_keyboard
)
from bot.config import ADMIN_IDS

router = Router()


class ManagePoints(StatesGroup):
    choosing_action = State()
    choosing_user = State()


class AddOpenResource(StatesGroup):
    section = State()
    title = State()
    description = State()
    link = State()
    city = State()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS


@router.message(F.text == "⚙️Admin Panel")
async def show_admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ You don't have access to this section.")
        return
    await message.answer(
        "⚙️ Admin Panel\n\nSelect an option:",
        reply_markup=get_admin_panel_keyboard()
    )


# ==================== MANAGE USERS ====================

@router.callback_query(F.data == "admin:users")
async def manage_users(callback: CallbackQuery, db: Database):
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
            f"Instagram: {user['instagram'] if user['instagram'] else 'none'}\n"
            f"💰 Points: {user['points']}\n"
            f"Registered: {user['registered_at'][:10]}\n\n"
        )
    if len(users_text) > 4096:
        chunks = [users_text[i:i+4096] for i in range(0, len(users_text), 4096)]
        await callback.message.answer(chunks[0])
        for chunk in chunks[1:]:
            await callback.message.answer(chunk)
    else:
        await callback.message.answer(users_text)
    await callback.answer()


# ==================== MODERATE LOTS ====================

@router.callback_query(F.data == "admin:lots")
async def moderate_lots_menu(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎁 Lots (Share)", callback_data="admin:lots_list:share"))
    builder.row(InlineKeyboardButton(text="🔍 Requests (Seek)", callback_data="admin:lots_list:seek"))
    builder.row(InlineKeyboardButton(text="⏳ Pending Moderation", callback_data="admin:lots_pending"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:back"))
    await callback.message.edit_text("🎯 Moderate Lots\n\nSelect:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("admin:lots_list:"))
async def show_lots_list(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lot_type = callback.data.split(":")[2]
    lots = await db.get_all_lots(lot_type)
    type_name = "Lots (Share)" if lot_type == "share" else "Requests (Seek)"
    if not lots:
        await callback.message.edit_text(
            f"🎯 {type_name}\n\n✅ No {lot_type} lots found.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]
            ])
        )
        await callback.answer()
        return
    # Show lots with delete buttons
    text = f"🎯 {type_name} ({len(lots)} total)\n\n"
    builder = InlineKeyboardBuilder()
    for lot in lots[:20]:  # limit to 20
        status_emoji = {"approved": "✅", "pending": "⏳", "rejected": "❌"}.get(lot['status'], "❓")
        text += (
            f"━━━━━━━━━━━━━━━\n"
            f"#{lot['id']} {status_emoji} {lot['title']}\n"
            f"👤 {lot['user_name']} | 📅 {lot['created_at'][:10]}\n"
        )
        builder.row(InlineKeyboardButton(
            text=f"🗑 Delete #{lot['id']} — {lot['title'][:30]}",
            callback_data=f"admin:lot_del:{lot['id']}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots"))
    if len(text) > 4096:
        text = text[:4090] + "..."
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("admin:lot_del:"))
async def delete_lot_admin(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await db.get_lot(lot_id)
    if not lot:
        await callback.answer("Lot not found", show_alert=True)
        return
    await db.admin_delete_lot(lot_id)
    await callback.answer(f"✅ Lot #{lot_id} deleted", show_alert=True)
    # Refresh the list
    lot_type = lot['type']
    lots = await db.get_all_lots(lot_type)
    type_name = "Lots (Share)" if lot_type == "share" else "Requests (Seek)"
    if not lots:
        await callback.message.edit_text(
            f"🎯 {type_name}\n\n✅ No lots remaining.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]
            ])
        )
        return
    text = f"🎯 {type_name} ({len(lots)} total)\n\n"
    builder = InlineKeyboardBuilder()
    for l in lots[:20]:
        status_emoji = {"approved": "✅", "pending": "⏳", "rejected": "❌"}.get(l['status'], "❓")
        text += f"━━━━━━━━━━━━━━━\n#{l['id']} {status_emoji} {l['title']}\n👤 {l['user_name']} | 📅 {l['created_at'][:10]}\n"
        builder.row(InlineKeyboardButton(text=f"🗑 Delete #{l['id']} — {l['title'][:30]}", callback_data=f"admin:lot_del:{l['id']}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots"))
    if len(text) > 4096:
        text = text[:4090] + "..."
    await callback.message.edit_text(text, reply_markup=builder.as_markup())


# Pending lots moderation (existing flow)
@router.callback_query(F.data == "admin:lots_pending")
async def show_pending_lots(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lots = await db.get_pending_lots()
    if not lots:
        await callback.message.edit_text(
            "🎯 Pending Moderation\n\n✅ No pending lots!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]
            ])
        )
        await callback.answer()
        return
    lot = lots[0]
    type_emoji = "🎁" if lot['type'] == "share" else "🔍"
    type_name = "Share" if lot['type'] == "share" else "Seek"
    await callback.message.edit_text(
        f"🎯 Pending ({len(lots)})\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 {lot['user_name']} (@{lot['username'] or 'none'})\n"
        f"📋 Type: {type_emoji} {type_name}\n\n"
        f"📌 {lot['title']}\n"
        f"📝 {lot['description']}\n"
        f"📅 {lot['created_at'][:10]}",
        reply_markup=get_lot_moderation_keyboard(lot['id'])
    )
    await callback.answer()


@router.callback_query(F.data == "admin:lots_next")
async def show_next_pending_lot(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lots = await db.get_pending_lots()
    if not lots:
        await callback.message.edit_text(
            "🎯 Pending Moderation\n\n✅ No more pending lots!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]
            ])
        )
        await callback.answer()
        return
    lot = lots[0]
    type_emoji = "🎁" if lot['type'] == "share" else "🔍"
    type_name = "Share" if lot['type'] == "share" else "Seek"
    await callback.message.edit_text(
        f"🎯 Pending ({len(lots)})\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 {lot['user_name']} (@{lot['username'] or 'none'})\n"
        f"📋 Type: {type_emoji} {type_name}\n\n"
        f"📌 {lot['title']}\n"
        f"📝 {lot['description']}\n"
        f"📅 {lot['created_at'][:10]}",
        reply_markup=get_lot_moderation_keyboard(lot['id'])
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lot:approve:"))
async def approve_lot(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await db.get_lot(lot_id)
    if not lot:
        await callback.answer("Lot not found", show_alert=True)
        return
    await db.update_lot_status(lot_id, "approved")
    try:
        await callback.bot.send_message(lot['user_id'], f"✅ Your lot has been approved!\n\n📌 {lot['title']}")
    except Exception:
        pass
    await callback.answer("✅ Lot approved!", show_alert=True)
    lots = await db.get_pending_lots()
    if lots:
        lot = lots[0]
        type_emoji = "🎁" if lot['type'] == "share" else "🔍"
        type_name = "Share" if lot['type'] == "share" else "Seek"
        await callback.message.edit_text(
            f"🎯 Pending ({len(lots)})\n\n━━━━━━━━━━━━━━━\n"
            f"👤 {lot['user_name']} (@{lot['username'] or 'none'})\n"
            f"📋 Type: {type_emoji} {type_name}\n\n📌 {lot['title']}\n📝 {lot['description']}\n📅 {lot['created_at'][:10]}",
            reply_markup=get_lot_moderation_keyboard(lot['id'])
        )
    else:
        await callback.message.edit_text("🎯 Pending Moderation\n\n✅ No more pending lots!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]]))


@router.callback_query(F.data.startswith("lot:reject:"))
async def reject_lot(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await db.get_lot(lot_id)
    if not lot:
        await callback.answer("Lot not found", show_alert=True)
        return
    await db.update_lot_status(lot_id, "rejected")
    try:
        await callback.bot.send_message(lot['user_id'], f"❌ Your lot was not approved.\n\n📌 {lot['title']}")
    except Exception:
        pass
    await callback.answer("❌ Lot rejected", show_alert=True)
    lots = await db.get_pending_lots()
    if lots:
        lot = lots[0]
        type_emoji = "🎁" if lot['type'] == "share" else "🔍"
        type_name = "Share" if lot['type'] == "share" else "Seek"
        await callback.message.edit_text(
            f"🎯 Pending ({len(lots)})\n\n━━━━━━━━━━━━━━━\n"
            f"👤 {lot['user_name']} (@{lot['username'] or 'none'})\n"
            f"📋 Type: {type_emoji} {type_name}\n\n📌 {lot['title']}\n📝 {lot['description']}\n📅 {lot['created_at'][:10]}",
            reply_markup=get_lot_moderation_keyboard(lot['id'])
        )
    else:
        await callback.message.edit_text("🎯 Pending Moderation\n\n✅ No more pending lots!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Back", callback_data="admin:lots")]]))


# ==================== MANAGE RESOURCES ====================

@router.callback_query(F.data == "admin:resources")
async def manage_resources(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    # Get all registration data to find which categories have resources
    all_data = await db.get_all_registration_data()
    # Count resources per category
    categories = {
        "selected_ra_items": "🏢 Businesses, Spaces & Platforms",
        "selected_skill_items": "🧑🏼‍💻 Skills",
        "selected_intro_items": "🤝🏻 Personal Introductions",
        "selected_property_types": "🗽 Real Estate",
        "selected_vehicle_types": "🖤 Cars",
        "selected_equipment_types": "🎧 Equipment",
        "selected_aircraft_types": "🛩️ Aircrafts",
        "selected_vessel_types": "💎 Boats",
        "specialists_list": "🩵 Specialists",
    }
    counts = {}
    for entry in all_data:
        try:
            reg = json.loads(entry['answer_data'])
            for key in categories:
                items = reg.get(key, [])
                if items:
                    counts[key] = counts.get(key, 0) + 1
        except:
            pass
    builder = InlineKeyboardBuilder()
    for key, name in categories.items():
        count = counts.get(key, 0)
        if count > 0:
            builder.row(InlineKeyboardButton(
                text=f"{name} ({count} users)",
                callback_data=f"admin:res_cat:{key}"
            ))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:back"))
    await callback.message.edit_text(
        "📦 Manage Resources\n\nCategories with user data:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:res_cat:"))
async def show_resource_category_users(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    cat_key = callback.data.split(":")[2]
    categories = {
        "selected_ra_items": "🏢 Businesses, Spaces & Platforms",
        "selected_skill_items": "🧑🏼‍💻 Skills",
        "selected_intro_items": "🤝🏻 Personal Introductions",
        "selected_property_types": "🗽 Real Estate",
        "selected_vehicle_types": "🖤 Cars",
        "selected_equipment_types": "🎧 Equipment",
        "selected_aircraft_types": "🛩️ Aircrafts",
        "selected_vessel_types": "💎 Boats",
        "specialists_list": "🩵 Specialists",
    }
    cat_name = categories.get(cat_key, cat_key)
    all_data = await db.get_all_registration_data()
    builder = InlineKeyboardBuilder()
    text = f"📦 {cat_name}\n\nUsers with resources:\n\n"
    user_count = 0
    for entry in all_data:
        try:
            reg = json.loads(entry['answer_data'])
            items = reg.get(cat_key, [])
            if items:
                user_count += 1
                name = entry['name']
                uid = entry['user_id']
                if isinstance(items, list) and len(items) > 0:
                    if isinstance(items[0], dict):
                        preview = f"{len(items)} entries"
                    else:
                        preview = ", ".join(items[:3])
                        if len(items) > 3:
                            preview += f"... (+{len(items)-3})"
                else:
                    preview = str(items)[:50]
                text += f"👤 {name} (ID: {uid})\n📋 {preview}\n\n"
                builder.row(InlineKeyboardButton(
                    text=f"🗑 Clear {name}'s {cat_name[:15]}",
                    callback_data=f"admin:res_del:{uid}:{cat_key}"
                ))
        except:
            pass
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:resources"))
    if len(text) > 4096:
        text = text[:4090] + "..."
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("admin:res_del:"))
async def delete_user_resource(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    parts = callback.data.split(":")
    uid = int(parts[2])
    cat_key = parts[3]
    # Get user's registration data, remove the category, save back
    answers = await db.get_user_answers(uid)
    for ans in answers:
        if ans['question_slug'] == 'registration_data':
            try:
                reg = json.loads(ans['answer_data'])
                if cat_key in reg:
                    reg[cat_key] = []
                    await db.add_user_answer(uid, 'registration_data', json.dumps(reg, default=str))
                    user = await db.get_user(uid)
                    await callback.answer(f"✅ Cleared {cat_key} for {user['name']}", show_alert=True)
                else:
                    await callback.answer("Category not found in user data", show_alert=True)
            except Exception as e:
                await callback.answer(f"Error: {e}", show_alert=True)
            break
    # Refresh the category view
    await show_resource_category_users(callback, db)


# ==================== MANAGE POINTS ====================

@router.callback_query(F.data == "admin:points")
async def manage_points_menu(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Add a Point", callback_data="admin:points_add"))
    builder.row(InlineKeyboardButton(text="➖ Remove a Point", callback_data="admin:points_remove"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:back"))
    await callback.message.edit_text("💰 Manage Points\n\nSelect action:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.in_({"admin:points_add", "admin:points_remove"}))
async def show_users_for_points(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    action = "add" if "add" in callback.data else "remove"
    users = await db.get_all_users()
    if not users:
        await callback.answer("No users found", show_alert=True)
        return
    action_text = "➕ Add a Point" if action == "add" else "➖ Remove a Point"
    builder = InlineKeyboardBuilder()
    for user in users:
        builder.row(InlineKeyboardButton(
            text=f"{user['name']} — {user['points']} pts",
            callback_data=f"admin:pt:{action}:{user['user_id']}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:points"))
    await callback.message.edit_text(
        f"💰 {action_text}\n\nSelect a user:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:pt:"))
async def adjust_user_points(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    parts = callback.data.split(":")
    action = parts[2]  # "add" or "remove"
    uid = int(parts[3])
    user = await db.get_user(uid)
    if not user:
        await callback.answer("User not found", show_alert=True)
        return
    current = user['points']
    new_points = current + 1 if action == "add" else max(0, current - 1)
    await db.update_user_points(uid, new_points)
    action_text = "+1" if action == "add" else "-1"
    await callback.answer(f"✅ {user['name']}: {current} → {new_points} ({action_text})", show_alert=True)
    # Refresh user list
    users = await db.get_all_users()
    action_label = "➕ Add a Point" if action == "add" else "➖ Remove a Point"
    builder = InlineKeyboardBuilder()
    for u in users:
        builder.row(InlineKeyboardButton(
            text=f"{u['name']} — {u['points']} pts",
            callback_data=f"admin:pt:{action}:{u['user_id']}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:points"))
    await callback.message.edit_text(f"💰 {action_label}\n\nSelect a user:", reply_markup=builder.as_markup())


# ==================== GENERATE TOKEN ====================

def generate_invite_token(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


@router.callback_query(F.data == "admin:generate_token")
async def generate_token(callback: CallbackQuery, db: Database):
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return
    token = generate_invite_token()
    success = await db.add_invite_token(token)
    if success:
        await callback.message.answer(
            f"🔑 New Invite Token\n\n`{token}`\n\nShare it with a new user to allow them to register."
        )
    else:
        await callback.message.answer("❌ Failed to generate a new token.")
    await callback.answer()


# ==================== BACK TO ADMIN PANEL ====================

@router.callback_query(F.data == "admin:back")
async def back_to_admin(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ Admin Panel\n\nSelect an option:",
        reply_markup=get_admin_panel_keyboard()
    )
    await callback.answer()
