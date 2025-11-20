# Community Telegram Bot

A Telegram bot for a closed international community platform with resource exchange and points system.

## Features

- **User Registration**: Collect user information including name, cities, about, and Instagram
- **Friends Section**: Browse community members by city
- **Resources Section**: Browse and share resources across multiple categories:
  - Real Estate
  - Cars
  - Aircrafts
  - Boats
  - Equipment
  - Skills and Knowledge
  - Experience and Time
  - Unique Opportunities
  - Works of Art
  - Personal Introduction to Specific Circles
- **Lots System**: Manage what you share and what you seek
- **Open Resources Database**: Shared maps, access links, and verified specialists
- **Points System**: Track member contributions
- **Admin Panel**: Manage users, resources, and points

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bottelegram
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and add your configuration:
- `BOT_TOKEN`: Your Telegram bot token from [@BotFather](https://t.me/BotFather)
- `ADMIN_IDS`: Comma-separated list of admin Telegram user IDs
- `CHANNEL_USERNAME`: Your community channel username (optional)
- `DATABASE_PATH`: Path to SQLite database file (default: bot_database.db)

## Getting Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token and paste it into `.env` file

## Getting Your User ID

To set yourself as an admin, you need your Telegram user ID:

1. Search for [@userinfobot](https://t.me/userinfobot) in Telegram
2. Start the bot and it will send you your user ID
3. Add this ID to `ADMIN_IDS` in `.env` file

## Running the Bot

```bash
python -p bot/main.py
```

Or using Python module:
```bash
python -m bot.main
```

## Project Structure

```
bottelegram/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Main bot entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database operations
│   ├── keyboards.py         # Keyboard layouts
│   └── handlers/            # Message handlers
│       ├── __init__.py
│       ├── registration.py  # User registration
│       ├── menu.py          # Main menu
│       ├── friends.py       # Friends section
│       ├── resources.py     # Resources section
│       ├── lots.py          # Lots section
│       ├── open_resources.py # Open resources
│       └── admin.py         # Admin panel
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## Database

The bot uses SQLite database with the following tables:

- **users**: User profiles with points
- **resources**: Community resources by category
- **lots**: User's shared and sought items
- **open_resources**: Shared maps, links, and specialists

Database is automatically created on first run.

## Admin Functions

Admins have access to additional features:

1. **Manage Users**: View all registered users
2. **Manage Points**: Update user points
3. **Manage Open Resources**: Add shared resources (maps, links, specialists)
4. **Manage Resources**: Moderate user-submitted resources (coming soon)

## Usage

### For Users

1. Start the bot with `/start`
2. Complete registration
3. Use the menu to:
   - Browse friends by city
   - Explore resources by category
   - Manage your lots (what you share/seek)
   - Access open resources database
   - View your profile

### For Admins

1. Access Admin Panel from the main menu
2. Manage users and their points
3. Add open resources for the community
4. Monitor resource submissions

## Bot Commands

- `/start` - Start the bot and register (or return to main menu)

## Points System

- Points are awarded for providing resources or services
- Each action equals one point
- Admins can manually adjust points through the admin panel
- Points are displayed on user profiles

## Channel Integration

The bot can link to a community channel for:
- News and updates
- Resident portraits
- Exchange digests
- New resource announcements

Configure `CHANNEL_USERNAME` in `.env` to enable this feature.

## Support

For issues or questions, contact the bot administrator.

## Technical Details

- **Framework**: aiogram 3.4.1
- **Database**: SQLite with aiosqlite
- **Python Version**: 3.8+
- **Async**: Full async/await support

## Development

The bot is structured for easy extension:

1. Add new handlers in `bot/handlers/`
2. Create new keyboard layouts in `bot/keyboards.py`
3. Add database methods in `bot/database.py`
4. Configure new features in `bot/config.py`

## License

This project is created for a private community. All rights reserved.
