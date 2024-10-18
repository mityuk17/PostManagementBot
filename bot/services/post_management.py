from datetime import datetime, timedelta
from schemas import Post
from botloader import bot_loader

from database.crud.channel import get_channel
from database.crud.post import get_post, update_post

from services.notifications import post_send_notification, post_delete_notification
from logs import logger

from keyboards import GeneralInlineKeyboard




def data_to_post(data: dict, user_id: int) -> Post:
    data["post_datetime"] = datetime.fromtimestamp(data.get("post_datetime"))
    data["delete_datetime"] = data["post_datetime"] + timedelta(hours=data.get("delete_hours"))

    new_post = Post(**data)
    
    return new_post


async def send_post(post: Post, chat_id: int) -> list[int]:
    messages = []
    if len(post.messages) > 1:
        messages = await bot_loader.tg_bot.copy_messages(
            chat_id=chat_id,
            from_chat_id=post.created_by,
            message_ids=sorted(post.messages),
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
        logger.no_messages_copied(post)
    
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
        bot_loader.scheduler.add_job(
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
    
    
async def cancel_posting(post_id: int):
    bot_loader.scheduler.remove_job(job_id=f"send-post_{post_id}")