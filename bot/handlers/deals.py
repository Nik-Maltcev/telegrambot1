from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.database import Database
from bot.keyboards import get_confirmation_keyboard, get_deal_completion_keyboard, get_menu_keyboard

router = Router()


@router.callback_query(F.data.startswith("deal:propose:"))
async def propose_deal(callback: CallbackQuery, db: Database):
    """Handle deal proposal."""
    receiver_id = int(callback.data.split(":")[-1])
    proposer_id = callback.from_user.id

    if proposer_id == receiver_id:
        await callback.answer("You cannot propose a deal to yourself.", show_alert=True)
        return

    deal_id = await db.create_deal(proposer_id, receiver_id)

    if deal_id:
        proposer = await db.get_user(proposer_id)
        receiver = await db.get_user(receiver_id)

        await callback.message.bot.send_message(
            receiver_id,
            f"🤝 New Deal Proposal\n\n"
            f"{proposer['name']} (@{proposer['username']}) has proposed a deal with you.\n\n"
            f"Do you accept?",
            reply_markup=get_confirmation_keyboard("deal", deal_id)
        )

        await callback.answer("Deal proposal sent!", show_alert=True)
    else:
        await callback.answer("Failed to propose the deal.", show_alert=True)


@router.callback_query(F.data.startswith("confirm:deal:"))
async def accept_deal(callback: CallbackQuery, db: Database):
    """Handle deal acceptance."""
    deal_id = int(callback.data.split(":")[-1])
    deal = await db.get_deal(deal_id)

    if not deal or deal['receiver_id'] != callback.from_user.id:
        await callback.answer("This deal is not for you.", show_alert=True)
        return

    if deal['status'] != 'pending':
        await callback.answer("This deal has already been responded to.", show_alert=True)
        return

    success = await db.update_deal_status(deal_id, "accepted")

    if success:
        proposer = await db.get_user(deal['proposer_id'])
        await callback.message.bot.send_message(
            deal['proposer_id'],
            f"✅ Deal Accepted\n\n"
            f"{callback.from_user.full_name} has accepted your deal proposal.",
            reply_markup=get_deal_completion_keyboard(deal_id)
        )
        await callback.message.edit_text("You have accepted the deal.")
    else:
        await callback.answer("Failed to accept the deal.", show_alert=True)


@router.callback_query(F.data.startswith("cancel:deal:"))
async def decline_deal(callback: CallbackQuery, db: Database):
    """Handle deal declination."""
    deal_id = int(callback.data.split(":")[-1])
    deal = await db.get_deal(deal_id)

    if not deal or deal['receiver_id'] != callback.from_user.id:
        await callback.answer("This deal is not for you.", show_alert=True)
        return

    if deal['status'] != 'pending':
        await callback.answer("This deal has already been responded to.", show_alert=True)
        return

    success = await db.update_deal_status(deal_id, "declined")

    if success:
        proposer = await db.get_user(deal['proposer_id'])
        await callback.message.bot.send_message(
            deal['proposer_id'],
            f"❌ Deal Declined\n\n"
            f"{callback.from_user.full_name} has declined your deal proposal."
        )
        await callback.message.edit_text("You have declined the deal.")
    else:
        await callback.answer("Failed to decline the deal.", show_alert=True)


@router.callback_query(F.data.startswith("deal:complete:"))
async def complete_deal(callback: CallbackQuery, db: Database):
    """Handle deal completion by the proposer."""
    deal_id = int(callback.data.split(":")[-1])
    deal = await db.get_deal(deal_id)

    if not deal or deal['proposer_id'] != callback.from_user.id:
        await callback.answer("This is not your deal to complete.", show_alert=True)
        return

    if deal['status'] != 'accepted':
        await callback.answer("This deal is not in an accepted state.", show_alert=True)
        return

    # Notify the receiver for confirmation
    receiver = await db.get_user(deal['receiver_id'])
    await callback.message.bot.send_message(
        deal['receiver_id'],
        f"🎉 Complete the Deal\n\n"
        f"{callback.from_user.full_name} has marked the deal as complete.\n"
        f"Please confirm to award them a point.",
        reply_markup=get_confirmation_keyboard("deal_confirm", deal_id)
    )
    await callback.message.edit_text("Request to complete the deal has been sent to the other party.")
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:deal_confirm:"))
async def confirm_deal_completion(callback: CallbackQuery, db: Database):
    """Handle deal completion confirmation by the receiver."""
    deal_id = int(callback.data.split(":")[-1])
    deal = await db.get_deal(deal_id)

    if not deal or deal['receiver_id'] != callback.from_user.id:
        await callback.answer("This is not your deal to confirm.", show_alert=True)
        return

    if deal['status'] != 'accepted':
        await callback.answer("This deal is not in an accepted state.", show_alert=True)
        return

    success = await db.update_deal_status(deal_id, "completed")

    if success:
        # Award point to the proposer
        proposer = await db.get_user(deal['proposer_id'])
        await db.update_user_points(deal['proposer_id'], proposer['points'] + 1)

        await callback.message.bot.send_message(
            deal['proposer_id'],
            f"Congratulations! You've earned a point for completing the deal with {callback.from_user.full_name}."
        )
        await callback.message.edit_text("You have confirmed the deal. A point has been awarded.")
    else:
        await callback.answer("Failed to confirm the deal.", show_alert=True)


@router.message(F.text == "📈 My Deals")
async def show_my_deals(message: Message, db: Database):
    """Show user's deal history."""
    deals = await db.get_user_deals(message.from_user.id)
    keyboard = get_menu_keyboard(message.from_user.id)

    if not deals:
        await message.answer("You have no deals yet.", reply_markup=keyboard)
        return

    deals_text = "📈 My Deals\n\n"
    for deal in deals:
        if deal['proposer_id'] == message.from_user.id:
            partner_name = deal['receiver_name']
            role = "Proposed"
        else:
            partner_name = deal['proposer_name']
            role = "Received"

        deals_text += (
            f"━━━━━━━━━━━━━━━\n"
            f"**Deal with:** {partner_name}\n"
            f"**Role:** {role}\n"
            f"**Status:** {deal['status'].capitalize()}\n"
            f"**Date:** {deal['created_at'][:10]}\n"
        )

    await message.answer(deals_text, reply_markup=keyboard)


@router.message(F.text.in_({"🔙 Back", "Back"}))
async def global_back_handler(message: Message):
    """Fallback handler for Back button if state is lost."""
    keyboard = get_menu_keyboard(message.from_user.id)
    await message.answer("Returning to main menu...", reply_markup=keyboard)
