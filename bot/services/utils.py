from botloader import bot_loader
from aiogram.types.chat_member_left import ChatMemberLeft
from aiogram.types.chat_member_administrator import ChatMemberAdministrator
from aiogram.types.chat_member_owner import ChatMemberOwner
from aiogram.types import Chat


async def is_subscribed(user_id: int, channel_id: int) -> bool:
    member = await bot_loader.tg_bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if isinstance(member, ChatMemberLeft):
        return False
    return True


async def is_channel_admin(user_id: int, channel_id: int) -> bool:
    member = await bot_loader.tg_bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if isinstance(member, ChatMemberAdministrator) or isinstance(member, ChatMemberOwner):
        return True
    else:
        return False


async def check_channel(channel_id: int) -> Chat | None:
    try:
        channel = await bot_loader.tg_bot.get_chat(chat_id=channel_id)
        
        return channel
 
    except:
        return None
