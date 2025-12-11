import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

# Admin configuration
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

# Debug: print admin IDs on startup
print(f"[DEBUG] ADMIN_IDS_STR: '{ADMIN_IDS_STR}'")
print(f"[DEBUG] ADMIN_IDS parsed: {ADMIN_IDS}")

# Channel configuration
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "")

# Database configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")

# Resource categories
RESOURCE_CATEGORIES = [
    "Real Estate",
    "Cars",
    "Aircrafts",
    "Boats",
    "Equipment",
    "Skills and Knowledge",
    "Experience and Time",
    "Unique Opportunities",
    "Works of Art",
    "Personal Introduction to Specific Circles"
]

# Open resources sections
OPEN_RESOURCES_SECTIONS = [
    "Google Maps",
    "Access Links",
    "Verified Specialists"
]
