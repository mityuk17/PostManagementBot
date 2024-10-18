from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram.fsm.context import FSMContext
from database.crud.channel import get_channel_by_user_and_channel_id, create_channel
from database.crud.user import get_user
from states import ChannelCreation
from schemas import Channel

from texts import channel_creation_texts
from keyboards import GeneralInlineKeyboard
from services.utils import check_channel, is_channel_admin


router = Router(name="ChannelCreation")


@router.callback_query(F.data == "new-channel")
async def new_channel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(ChannelCreation.channel_id)
    
    await callback.message.answer(
        text=channel_creation_texts.get_channel_id(),
        reply_markup=GeneralInlineKeyboard.cancel()
    )
    await callback.message.delete()
    

@router.message(ChannelCreation.channel_id)
async def get_channel_id(message: Message, state: FSMContext):
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
    else:
        try:
            channel_id = int(message.text.split())
        except ValueError:
            await message.answer(
                text=channel_creation_texts.invalid_channel_id(),
                reply_markup=GeneralInlineKeyboard.cancel())
            
    channel = await check_channel(channel_id)
    
    #Проверка нахождения канала ботом
    if not channel:
        await message.answer(
            text=channel_creation_texts.channel_not_found(),
            reply_markup=GeneralInlineKeyboard.cancel()
        )
    
    #Проверка пользователя на админа в канале
    if not(is_channel_admin(message.from_user.id, channel_id)):
        await message.answer(
            text=channel_creation_texts.not_channel_admin(),
            reply_markup=GeneralInlineKeyboard.cancel()
        )
    
    #Проверка на уникальность
    if (await get_channel_by_user_and_channel_id(channel_id, message.from_user.id)):
        await message.answer(
            text=channel_creation_texts.channel_already_exists(),
            reply_markup=GeneralInlineKeyboard.cancel()
        )
    
    new_channel = Channel(
        channel_id=channel_id,
        added_by=message.from_user.id,
        title=channel.title,
    )
    
    await create_channel(new_channel)
    await state.clear()
    
    await message.answer(
        text=channel_creation_texts.channel_created(new_channel.title),
        reply_markup=GeneralInlineKeyboard.back()
    )
            
    