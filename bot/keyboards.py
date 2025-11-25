from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="👥 Friends"),
        KeyboardButton(text="📦 Resources")
    )
    builder.row(
        KeyboardButton(text="🎯 Lots"),
        KeyboardButton(text="📢 Channel")
    )
    builder.row(
        KeyboardButton(text="🗂 Open Resources Database"),
        KeyboardButton(text="👤 My Profile")
    )
    builder.row(
        KeyboardButton(text="📈 My Deals")
    )
    return builder.as_markup(resize_keyboard=True)


def get_admin_menu_keyboard() -> ReplyKeyboardMarkup:
    """Admin menu keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="👥 Friends"),
        KeyboardButton(text="📦 Resources")
    )
    builder.row(
        KeyboardButton(text="🎯 Lots"),
        KeyboardButton(text="📢 Channel")
    )
    builder.row(
        KeyboardButton(text="🗂 Open Resources Database"),
        KeyboardButton(text="👤 My Profile")
    )
    builder.row(
        KeyboardButton(text="📈 My Deals"),
        KeyboardButton(text="⚙️ Admin Panel")
    )
    return builder.as_markup(resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Cancel keyboard"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔙 Back"))
    return builder.as_markup(resize_keyboard=True)


def get_cities_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with city buttons"""
    cities = [
        "Paris", "Berlin", "New York", "Lisbon", "Amsterdam", "Budapest",
        "Bangkok", "Tokyo", "Barcelona", "Istanbul", "London", "Warsaw", "Minsk"
    ]
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.row(InlineKeyboardButton(text=city, callback_data=f"city:{city}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main_menu"))
    return builder.as_markup()


def get_resource_categories_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with resource categories"""
    categories = [
        ("🏠 Real Estate", "res_cat:Real Estate"),
        ("🚗 Cars", "res_cat:Cars"),
        ("✈️ Aircrafts", "res_cat:Aircrafts"),
        ("⛵ Boats", "res_cat:Boats"),
        ("🔧 Equipment", "res_cat:Equipment"),
        ("🎓 Skills and Knowledge", "res_cat:Skills and Knowledge"),
        ("⏰ Experience and Time", "res_cat:Experience and Time"),
        ("✨ Unique Opportunities", "res_cat:Unique Opportunities"),
        ("🎨 Works of Art", "res_cat:Works of Art"),
        ("🤝 Personal Introduction", "res_cat:Personal Introduction to Specific Circles"),
    ]

    builder = InlineKeyboardBuilder()
    for text, callback_data in categories:
        builder.row(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_resources"))
    return builder.as_markup()


def get_lots_type_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting lot type"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 I Share", callback_data="lots:share"),
        InlineKeyboardButton(text="🔍 I Seek", callback_data="lots:seek")
    )
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu"))
    return builder.as_markup()


def get_open_resources_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for open resources sections"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗺 Google Maps", callback_data="open:maps"))
    builder.row(InlineKeyboardButton(text="🔑 Access Links", callback_data="open:accesses"))
    builder.row(InlineKeyboardButton(text="👨‍💼 Verified Specialists", callback_data="open:specialists"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu"))
    return builder.as_markup()


def get_back_keyboard(callback_data: str = "back_to_menu") -> InlineKeyboardMarkup:
    """Simple back button"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data=callback_data))
    return builder.as_markup()


def get_user_card_keyboard(user_id: int, instagram: str = "") -> InlineKeyboardMarkup:
    """Keyboard for user card"""
    builder = InlineKeyboardBuilder()
    if instagram:
        builder.row(InlineKeyboardButton(text="📸 Instagram", url=f"https://instagram.com/{instagram.lstrip('@')}"))
    builder.row(InlineKeyboardButton(text="💬 Contact", url=f"tg://user?id={user_id}"))
    builder.row(InlineKeyboardButton(text="🤝 Propose Deal", callback_data=f"deal:propose:{user_id}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_friends"))
    return builder.as_markup()


def get_resource_card_keyboard(owner_id: int, instagram: str = "") -> InlineKeyboardMarkup:
    """Keyboard for resource card"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💬 Request / Contact", url=f"tg://user?id={owner_id}"))
    builder.row(InlineKeyboardButton(text="🤝 Propose Deal", callback_data=f"deal:propose:{owner_id}"))
    if instagram:
        builder.row(InlineKeyboardButton(text="📸 Instagram", url=f"https://instagram.com/{instagram.lstrip('@')}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_category"))
    return builder.as_markup()


def get_add_lot_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for adding new lot"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Add New", callback_data="add_lot"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="lots_menu"))
    return builder.as_markup()


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Admin panel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👥 Manage Users", callback_data="admin:users"))
    builder.row(InlineKeyboardButton(text="📦 Manage Resources", callback_data="admin:resources"))
    builder.row(InlineKeyboardButton(text="🗂 Manage Open Resources", callback_data="admin:open_resources"))
    builder.row(InlineKeyboardButton(text="💰 Manage Points", callback_data="admin:points"))
    builder.row(InlineKeyboardButton(text="🔑 Generate Invite Token", callback_data="admin:generate_token"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu"))
    return builder.as_markup()


def get_confirmation_keyboard(action: str, item_id: int = 0) -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm:{action}:{item_id}"),
        InlineKeyboardButton(text="❌ No", callback_data=f"cancel:{action}")
    )
    return builder.as_markup()


def get_deal_completion_keyboard(deal_id: int) -> InlineKeyboardMarkup:
    """Keyboard for deal completion."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Mark as Complete", callback_data=f"deal:complete:{deal_id}")
    )
    return builder.as_markup()
