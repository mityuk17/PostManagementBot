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
from services.post_management import data_to_post


router = Router(name="General")


@router.message(Command("start"))
@router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=general_texts.menu(), reply_markup=GeneralInlineKeyboard.menu())
    

@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer(
        text=general_texts.menu(),
        reply_markup=GeneralInlineKeyboard.menu()
    )
    
    await callback.message.delete()
    

@router.callback_query(F.data.startswith("check-subscription_"))
async def check_subscription_button(callback: CallbackQuery, state: FSMContext):
    
    post_id = callback.data.split("_")[-1]
    if post_id == "preview":
        post = data_to_post(await state.get_data(), callback.from_user.id)
    else:
        post = await get_post(int(post_id))
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