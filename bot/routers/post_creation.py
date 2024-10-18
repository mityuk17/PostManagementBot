from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.crud.channel import get_channel, all_channels
from database.crud.post import create_post
from states import PostCreation
from texts import post_creation_texts
from keyboards import GeneralInlineKeyboard, PostCreationInlineKeyboard
from services.utils import is_url
from services.post_management import data_to_post, post_preview, scheduled_post
from aiogram_media_group import media_group_handler
import re
from datetime import datetime
from botloader import bot_loader


router = Router(name="PostCreation")


@router.callback_query(F.data == "new-post")
async def start_post_creation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    channels = await all_channels(user_id=callback.from_user.id)
    
    await state.set_state(PostCreation.channel_id)
    await callback.message.answer(
        text=post_creation_texts.pick_target_channel(),
        reply_markup=PostCreationInlineKeyboard.pick_target_channel(channels))
    await callback.message.delete()
    

@router.callback_query(F.data.startswith("channel-id_"), PostCreation.channel_id)
async def get_channel_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    channel_id = int(callback.data.split("_")[-1])
    channel = await get_channel(channel_id)
    
    await state.update_data({"target_channel_id": channel_id})
    await state.set_state(PostCreation.messages)
    
    await callback.message.edit_text(
        text=post_creation_texts.picked_target_channel(channel.title),
        reply_markup=None
    )
    await callback.message.answer(
        text=post_creation_texts.get_messages(),
        reply_markup=GeneralInlineKeyboard.cancel()
    )
    

@router.message(PostCreation.messages)
@media_group_handler(only_album=False)
async def get_messages_media_group(messages: list[Message], state: FSMContext):
    messages_ids = [message.message_id for message in messages]
    await state.update_data({"messages": messages_ids})
    if len(messages) > 1:
        await messages[0].answer(
            text=post_creation_texts.got_media_group()
        )
        await state.set_state(PostCreation.send_without_notification)
    
        await messages[0].answer(
            text=post_creation_texts.pick_without_notification(),
            reply_markup=PostCreationInlineKeyboard.pick_without_notification()
        )
    else:
        await state.set_state(PostCreation.button_type)
        await messages[0].answer(
        text=post_creation_texts.pick_button_type(),
        reply_markup=PostCreationInlineKeyboard.pick_button_type()
    )

# @router.message(PostCreation.messages)
# async def get_one_message(message: Message, state: FSMContext):
#     await state.update_data({"messages": [message.message_id]})
#     await state.set_state(PostCreation.button_type)
#     await message.answer(
#         text=post_creation_texts.pick_button_type(),
#         reply_markup=PostCreationInlineKeyboard.pick_button_type()
#     )


@router.callback_query(F.data.startswith("button-type_"))
async def pick_button_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    button_type = callback.data.split("_")[-1]
    await callback.message.edit_text(text=post_creation_texts.picked_button_type(button_type))
    
    if button_type == "no":
        await state.set_state(PostCreation.send_without_notification)
        await callback.message.answer(
            text=post_creation_texts.pick_without_notification(),
            reply_markup=PostCreationInlineKeyboard.pick_without_notification()
        )
    elif button_type == "check-subscription":
        await state.set_state(PostCreation.button_subscribed_text)
        await callback.message.edit_text(
            text=post_creation_texts.get_button_subscribed_text(),
            reply_markup=GeneralInlineKeyboard.cancel()
        )
    elif button_type == "url":
        await state.set_state(PostCreation.button_url)
        await callback.message.edit_text(
            text=post_creation_texts.get_button_url(),
            reply_markup=GeneralInlineKeyboard.cancel()
        )


@router.message(PostCreation.button_subscribed_text)
async def get_button_subscribed_text(message: Message, state: FSMContext):
    await state.update_data({"button_subscribed_text": message.text.strip()})
    await state.set_state(PostCreation.button_unsubscribed_text)
    
    await message.answer(
        text=post_creation_texts.get_button_unsubscribed_text(),
        reply_markup=GeneralInlineKeyboard.cancel()
    )


@router.message(PostCreation.button_unsubscribed_text)
async def get_button_unsubscribed_text(message: Message, state: FSMContext):
    await state.update_data({"button_unsubscribed_text": message.text.strip()})
    await state.set_state(PostCreation.button_label)
    
    await message.answer(
        text=post_creation_texts.get_button_label(),
        reply_markup=GeneralInlineKeyboard.cancel()
    )


@router.message(PostCreation.button_url)
async def get_button_url(message: Message, state: FSMContext):
    await state.update_data({"button_url": message.text.strip()})
    await state.set_state(PostCreation.button_label)
    
    await message.answer(
        text=post_creation_texts.get_button_label(),
        reply_markup=GeneralInlineKeyboard.cancel()
    )


@router.message(PostCreation.button_label)
async def get_button_label(mesage: Message, state: FSMContext):
    await state.update_data({"button_label": mesage.text.strip()})
    await state.set_state(PostCreation.send_without_notification)
    
    await mesage.answer(
        text=post_creation_texts.pick_without_notification(),
        reply_markup=PostCreationInlineKeyboard.pick_without_notification()
    )


@router.callback_query(F.data.startswith("without-notification_"), PostCreation.send_without_notification)
async def pick_without_notification(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    send_without_notification = True if callback.data.split("_")[-1] == "yes" else False
    await state.update_data({"send_without_notification": send_without_notification})
    
    await callback.message.edit_text(
        text=post_creation_texts.picked_without_notification(send_without_notification),
        reply_markup=None
    )
    
    await state.set_state(PostCreation.post_datetime)
    await callback.message.answer(
        text=post_creation_texts.get_post_datetime(),
        reply_markup=GeneralInlineKeyboard.cancel())


@router.message(PostCreation.post_datetime)
async def get_post_datetime(message: Message, state: FSMContext):
    if not re.fullmatch(r"\d{1,2}.\d{1,2}.\d{4} \d{1,2}:\d{2}", message.text.strip()):
        await message.answer(post_creation_texts.invalid_post_datetime())
        return
    post_datetime = datetime.strptime(message.text.strip(), "%d.%m.%Y %H:%M")
    
    await state.update_data({"post_datetime": post_datetime.timestamp()})
    await state.set_state(PostCreation.delete_datetime)
    
    await message.answer(
        text=post_creation_texts.get_delete_hours(),
        reply_markup=PostCreationInlineKeyboard.pick_delete_datetime()
    )


@router.message(PostCreation.delete_datetime)
async def get_delete_datetime(message: Message, state: FSMContext):
    if not message.text.strip().isdigit():
        await message.answer(post_creation_texts.invalid_delete_hours())
        return
    delete_hours = int(message.text.strip())
    
    await state.update_data({"delete_hours": delete_hours})
    await state.set_state(PostCreation.preview_check)
    
    post_data = data_to_post((await state.get_data()), message.from_user.id)
    await post_preview(post_data)
    await message.answer(
        text=post_creation_texts.post_preview_info(),
        reply_markup=PostCreationInlineKeyboard.preview_check()
    )


@router.callback_query(F.data.startswith("delete-datetime_"))
async def get_delete_datetime_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    delete_hours = callback.data.split("_")[-1]
    delete_hours = int(delete_hours) if delete_hours != "no" else 0
    
    await state.update_data({"delete_hours": delete_hours})
    await state.set_state(PostCreation.preview_check)
    
    await callback.message.edit_text(
        text=post_creation_texts.picked_delete_hours(delete_hours),
        reply_markup=None
    )
    
    post_data = data_to_post((await state.get_data()), callback.from_user.id)
    await post_preview(post_data)
    await callback.message.answer(
        text=post_creation_texts.post_preview_info(),
        reply_markup=PostCreationInlineKeyboard.preview_check()
    )


@router.callback_query(F.data == "save-post")
async def save_post(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    post_data = data_to_post((await state.get_data()), callback.from_user.id)
    
    created_post = await create_post(post_data)
    await state.clear()
    
    await callback.message.edit_text(
        text=post_creation_texts.post_confirmation(),
        reply_markup=None
    )
    
    bot_loader.scheduler.add_job(
        id=f"send-post_{created_post.id}",
        func=scheduled_post,
        args=[created_post.id],
        trigger="date",
        run_date=created_post.post_datetime,
        coalesce=True
    )


@router.callback_query(F.data == "cancel-post")
async def cancel_post(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    
    await callback.message.edit_text(
        text=post_creation_texts.post_cancelled(),
    )