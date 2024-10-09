from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram.fsm.context import FSMContext
from database.crud.channel import all_channels, get_channel, update_channel, delete_channel
from database.crud.user import get_user
from schemas import UserRole
from texts import general_texts
from keyboards import GeneralInlineKeyboard
from logs import logger


router = Router(name="ChannelManagement")


@router.callback_query(F.data == "channels")
async def channels_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text=general_texts.menu(),
        reply_markup=GeneralInlineKeyboard.channels_menu()
    )


@router.inline_query(F.query == "Каналы")
async def list_channels(query: InlineQuery):
    user = await get_user(query.from_user.id)
    channels = await all_channels(
        only_active=False,
        user_id=user.id if user.role != UserRole.Admin else None)
    
    response = []
    
    offset = int(query.offset) if query.offset else 0
    
    for channel in channels[offset:offset+50]:
        description = f"""Статус: {"✅Подключен" if channel.active else "❌Отключен"}
<i>channel_id</i>: {channel.channel_id}"""
        if user.role == UserRole.Admin:
            description += f"\nДобавлен пользователем {channel.added_by}"
        response.append(InlineQueryResultArticle(
            id=str(channel.id),
            title=channel.title,
            input_message_content=InputTextMessageContent(f"/channel {channel.id}"),
            description=description
        ))
    
    await query.answer(
        results=response,
        cache_time=5,
        is_personal=True,
        next_offset=str(offset+50)
    )
    
    
@router.message(F.text.startswith("/channel "))
async def show_channel(message: Message):
    channel_id = int(message.text.split()[-1])
    channel = await get_channel(channel_id)
    user = await get_user(message.from_user.id)
    if not((user.role == UserRole.Admin) or (user.id == channel.added_by)):
        return
    
    await message.reply(
        text=general_texts.channel_info(channel, user.role == UserRole.Admin),
        reply_markup=GeneralInlineKeyboard.channel_actions(channel.channel_id, is_active=channel.active)
    )
    

@router.callback_query(F.data.startswith("switch-channel_"))
async def switch_channel(callback: CallbackQuery):
    await callback.answer()
    channel_id = int(callback.data.split("_")[-1])
    channel = await get_channel(channel_id)
    channel.active = not(channel.active)
    await update_channel(channel)
    user = await get_user(callback.from_user.id)
    
    if not((user.role == UserRole.Admin) or (user.id == channel.added_by)):
        return
    
    await callback.message.edit_text(
        text=general_texts.channel_info(channel, user.role == UserRole.Admin),
        reply_markup=GeneralInlineKeyboard.channel_actions(channel.channel_id, is_active=channel.active)
    )
    

@router.callback_query(F.data.startswith("remove-channel_"))
async def remove_channel(callback: CallbackQuery):
    await callback.answer()
    
    channel_id = int(callback.data.split("_")[-1])
    channel = await get_channel(channel_id)
    await delete_channel(channel_id)
    await logger.channel_removed(channel)
    await callback.message.edit_text(
        text=general_texts.channel_removed(),
        reply_markup=GeneralInlineKeyboard.back()
    )