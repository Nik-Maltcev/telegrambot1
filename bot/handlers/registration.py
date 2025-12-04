from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InputFile
from bot.database import Database
from bot.keyboards import get_main_menu_keyboard, get_admin_menu_keyboard, get_cancel_keyboard
from bot.config import ADMIN_IDS

router = Router()


class Registration(StatesGroup):
    name = State()
    main_city = State()
    about = State()
    current_city = State()
    instagram = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database):
    """Handle /start command"""
    user = await db.get_user(message.from_user.id)

    if user:
        # User already registered
        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()

        await message.answer(
            f"👋 Welcome back, {user['name']}!\n\n"
            f"Choose an option from the menu below:",
            reply_markup=keyboard
        )
    else:
        # New user - check for invite token or if admin
        is_admin = message.from_user.id in ADMIN_IDS
        args = message.text.split()

        if is_admin:
            # Allow admin to register without token
            await message.answer(
                "👋 Welcome Admin!\n\n"
                "Let's get you registered!\n\n"
                "Please enter your name:",
                reply_markup=get_cancel_keyboard()
            )
            await state.set_state(Registration.name)
            return

        if len(args) > 1:
            token = args[1]
            if await db.is_valid_token(token):
                await state.update_data(invite_token=token)
                # Start registration
                video_url = "https://www.youtube.com/watch?v=z1MgFIpSqJk&list=RDz1MgFIpSqJk&start_radio=1"
                await message.answer_video(
                    video=video_url,
                    caption=(
                        "👋 Welcome to the Community!\n\n"
                        "This is a closed international community for talented, successful, "
                        "and aspiring people who are ready to share their resources and skills "
                        "on a voluntary basis.\n\n"
                        "Let's get you registered!\n\n"
                        "Please enter your name:"
                    ),
                    reply_markup=get_cancel_keyboard()
                )
                await state.set_state(Registration.name)
            else:
                await message.answer("❌ Invalid or expired invite token.")
        else:
            await message.answer(
                "👋 Welcome to the Community!\n\n"
                "This is a private community. To join, you need an invite token.\n"
                "Please use the invite link from an admin to register."
            )


@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext):
    """Process name input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(name=message.text)
    await message.answer(
        "Great! Now, please enter the city where you are usually located:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.main_city)


@router.message(Registration.main_city, F.text)
async def process_main_city(message: Message, state: FSMContext):
    """Process main city input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(main_city=message.text)
    await message.answer(
        "Tell us a bit about yourself (brief intro):\n\n"
        "For example •Artist and community owner•",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.about)


@router.message(Registration.about, F.text)
async def process_about(message: Message, state: FSMContext):
    """Process about input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(about=message.text)
    await message.answer(
        "What is your current city?",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.current_city)


@router.message(Registration.current_city, F.text)
async def process_current_city(message: Message, state: FSMContext):
    """Process current city input"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    await state.update_data(current_city=message.text)
    await message.answer(
        "Please enter your Instagram username (or send '-' if you don't have one):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Registration.instagram)


@router.message(Registration.instagram, F.text)
async def process_instagram(message: Message, state: FSMContext, db: Database):
    """Process Instagram and complete registration"""
    if message.text == "🔙 Back":
        await state.clear()
        await message.answer("Registration cancelled.", reply_markup=None)
        return

    instagram = message.text if message.text != "-" else ""
    data = await state.get_data()

    # Save user to database
    success = await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=data['name'],
        main_city=data['main_city'],
        current_city=data['current_city'],
        about=data['about'],
        instagram=instagram,
        points=0  # Starting with 0 points
    )

    if success:
        # Mark token as used if it was present
        if 'invite_token' in data:
            await db.use_invite_token(data['invite_token'])

    await state.clear()

    if success:
        is_admin = message.from_user.id in ADMIN_IDS
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()

        await message.answer(
            f"🩵 Registration completed!\n\n"
            f"👀Name: {data['name']}\n"
            f"📍Main City: {data['main_city']}\n"
            f"🗽Current City: {data['current_city']}\n"
            f"💌About: {data['about']}\n"
            f"💿Instagram: @{instagram if instagram else 'Not provided'}\n"
            f"Points: 0",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "❌ An error occurred during registration. Please try again with /start"
        )
