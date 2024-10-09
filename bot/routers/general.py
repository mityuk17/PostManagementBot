from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from texts import general_texts
from database.crud.post import get_post
from database.crud.channel import get_channel
from services.utils import is_subscribed
from keyboards import GeneralInlineKeyboard
from botloader import bot_loader


router = Router(name="General")


@router.message(Command("start") | Command("menu"))
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=general_texts.menu(), reply_markup=GeneralInlineKeyboard.menu())
    

@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    for msg_id in (await state.get_data()).get("edit_reply_markup_messages", []):
        await bot_loader.tg_bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=msg_id,
            reply_markup=None
        )
    
    await callback.message.answer(
        text=general_texts.menu(),
        reply_markup=GeneralInlineKeyboard.menu()
    )
    

@router.callback_query(F.data.startswith("check-subscription_"))
async def check_subscription_button(callback: CallbackQuery):
    post_id = int(callback.data.split("_")[-1])
    post = await get_post(post_id)
    if not post:
        return
    channel = await get_channel(post.target_channel_id)
    if not channel:
        return
    if (await is_subscribed(callback.from_user.id, channel.channel_id)):
        text = post.button_subscribed_text
    else:
        text = post.button_unsubscribed_text
    
    await callback.answer(text, show_alert=True)