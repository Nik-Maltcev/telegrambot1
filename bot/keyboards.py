from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List, Dict, Set
from bot.config import ADMIN_IDS
from bot.form_data import SKILL_CATEGORIES, OFFER_FORMATS, INTERACTION_FORMATS, RESULT_TYPES


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
        "New York", "Los Angeles", "San Francisco", "Miami",
        "London", "Paris", "Berlin", "Hamburg", "Amsterdam",
        "Milan", "Rome", "Barcelona", "Copenhagen", "Stockholm", "Lisbon",
        "Vienna", "Zurich", "Prague", "Budapest", "Warsaw", "Moscow",
        "Bangkok", "Singapore", "Hong Kong", "Tokyo", "Seoul",
        "Shanghai", "Beijing", "Dubai",
        "Sydney", "Melbourne",
        "Mexico City", "São Paulo", "Buenos Aires", "Rio de Janeiro",
        "Tel Aviv", "Istanbul"
    ]
    builder = InlineKeyboardBuilder()
    # Create rows with 2 columns for better visibility
    for i in range(0, len(cities), 2):
        row_btns = []
        row_btns.append(InlineKeyboardButton(text=cities[i], callback_data=f"city:{cities[i]}"))
        if i + 1 < len(cities):
            row_btns.append(InlineKeyboardButton(text=cities[i+1], callback_data=f"city:{cities[i+1]}"))
        builder.row(*row_btns)

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


def get_create_lot_type_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting lot type to create"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 I Share", callback_data="create_lot:share"),
        InlineKeyboardButton(text="🔍 I Seek", callback_data="create_lot:seek")
    )
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="lots_menu"))
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
    builder.row(InlineKeyboardButton(text="🎯 Moderate Lots", callback_data="admin:lots"))
    builder.row(InlineKeyboardButton(text="📦 Manage Resources", callback_data="admin:resources"))
    builder.row(InlineKeyboardButton(text="🗂 Manage Open Resources", callback_data="admin:open_resources"))
    builder.row(InlineKeyboardButton(text="💰 Manage Points", callback_data="admin:points"))
    builder.row(InlineKeyboardButton(text="🔑 Generate Invite Token", callback_data="admin:generate_token"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu"))
    return builder.as_markup()


def get_lot_moderation_keyboard(lot_id: int) -> InlineKeyboardMarkup:
    """Keyboard for lot moderation"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Approve", callback_data=f"lot:approve:{lot_id}"),
        InlineKeyboardButton(text="❌ Reject", callback_data=f"lot:reject:{lot_id}")
    )
    builder.row(InlineKeyboardButton(text="⏭ Skip", callback_data="admin:lots_next"))
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


def get_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Get the correct menu keyboard for a user."""
    if user_id in ADMIN_IDS:
        return get_admin_menu_keyboard()
    return get_main_menu_keyboard()


# --- Questionnaire Keyboards ---

def get_skill_categories_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting skill category (Single Choice)"""
    builder = InlineKeyboardBuilder()
    for key, data in SKILL_CATEGORIES.items():
        # Truncate long names if necessary or use code
        text = f"{key}. {data['name']}"
        builder.row(InlineKeyboardButton(text=text, callback_data=f"q_cat:{key}"))

    return builder.as_markup()

def get_skill_items_keyboard(category_key: str, selected: Set[str]) -> InlineKeyboardMarkup:
    """Keyboard for selecting skill items (Multiple Choice)"""
    builder = InlineKeyboardBuilder()
    items = SKILL_CATEGORIES.get(category_key, {}).get("items", [])

    for item in items:
        is_selected = item in selected
        text = f"{'✅' if is_selected else '⬜️'} {item}"
        # Store index to save space in callback data, or use hash?
        # Using simplified slug or index might be risky if list changes.
        # Let's try to use short identifier.
        # Actually, callback_data limit is 64 chars. Some items are long.
        # We need a way to map them.
        import hashlib
        item_hash = hashlib.md5(item.encode()).hexdigest()[:8]
        builder.row(InlineKeyboardButton(text=text, callback_data=f"q_item:{item_hash}"))

    builder.row(InlineKeyboardButton(text="🆗 Done", callback_data="q_item_done"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="q_back_cat"))
    return builder.as_markup()

def get_multiselect_keyboard(options: List[str], selected: Set[str], prefix: str, done_callback: str) -> InlineKeyboardMarkup:
    """Generic multiselect keyboard"""
    builder = InlineKeyboardBuilder()
    import hashlib

    for item in options:
        is_selected = item in selected
        text = f"{'✅' if is_selected else '⬜️'} {item}"
        item_hash = hashlib.md5(item.encode()).hexdigest()[:8]
        builder.row(InlineKeyboardButton(text=text, callback_data=f"{prefix}:{item_hash}"))

    builder.row(InlineKeyboardButton(text="🆗 Done", callback_data=done_callback))
    return builder.as_markup()
