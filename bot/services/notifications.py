from botloader import bot_loader
from schemas import Post, Channel
from database.crud.channel import get_channel
from texts import notifications_texts


async def post_send_notification(post: Post):
    channel = await get_channel(post.target_channel_id)
    
    await bot_loader.tg_bot.send_message(
        chat_id=post.created_by,
        text=notifications_texts.post_send(post, channel)
    )
    

async def post_delete_notification(post: Post):
    channel = await get_channel(post.target_channel_id)
    
    await bot_loader.tg_bot.send_message(
        chat_id=post.created_by,
        text=notifications_texts.post_delete(post, channel)
    )