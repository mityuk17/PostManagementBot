from schemas import Post
from botloader import bot_loader
from aiogram.utils.media_group import MediaGroupBuilder
from database.crud.channel import get_channel
from database.crud.post import get_post, update_post
from keyboards import GeneralInlineKeyboard
from datetime import timedelta
from services.notifications import post_send_notification, post_delete_notification
from datetime import datetime, timedelta


def data_to_post(data: dict, user_id: int) -> Post:
    post_datetime = datetime.strptime(data.get("post_datetime"), "%d.%m.%Y %H:%M") if data.get("post_datetime") else datetime.now()
    delete_datetime = post_datetime + timedelta(hours=data.get("delete_hours"))

    new_post = Post(
        messages=data.get("messages"),
        created_by=user_id,
        target_channel_id=data.get("target_channel_id"),
        button_label=data.get("button_label"),
        button_subscribed_text=data.get("button_subscribed_text"),
        button_unsubscribed_text=data.get("button_unsubscribed_text"),
        button_url=data.get("button_url"),
        send_without_notification=data.get("with_notification"),
        post_datetime=post_datetime,
        delete_datetime=delete_datetime
    )
    
    return new_post


async def send_post(post: Post, chat_id: int) -> list[int]:
    messages = []
    if len(post.messages) > 1:
        messages = await bot_loader.tg_bot.copy_messages(
            chat_id=chat_id,
            from_chat_id=post.created_by,
            message_ids=post.messages,
            disable_notification=post.send_without_notification
        )
    else:
        message_id = await bot_loader.tg_bot.copy_message(
            chat_id=chat_id,
            from_chat_id=post.created_by,
            message_id=post.messages[0],
            reply_markup=GeneralInlineKeyboard.post_button(post),
            disable_notification=post.send_without_notification
        )
        messages.append(message_id)
    
    if not messages:
        ...
    
    return messages


async def post_preview(post: Post):
    await send_post(post, post.created_by)
    

async def scheduled_post(post_id):
    post = await get_post(post_id)
    if not post:
        return

    channel = await get_channel(post.target_channel_id)
    messages = await send_post(post, channel.channel_id)
    await post_send_notification(post)
    
    post.posted = True
    await update_post(post)
    
    if post.delete_datetime:
        await bot_loader.scheduler.add_job(
            id=f"delete-post_{post_id}",
            func=autodelete_post,
            args=[post_id, messages],
            trigger="date",
            run_date=post.delete_datetime,
            coalesce=True
        )
    

async def autodelete_post(post_id: int, messages_ids: int):
    post = await get_post(post_id)
    if not post:
        return
    channel = await get_channel(post.target_channel_id)
    
    is_deleted = (await bot_loader.tg_bot.delete_messages(chat_id=channel.channel_id, message_ids=messages_ids))
    post.deleted = is_deleted
    await update_post(post)
    
    await post_delete_notification(post)
    
    
    