from botloader import bot_loader
from schemas import Channel
from sqlmodel import select, delete, update


async def create_channel(channel_data: Channel) -> Channel:
    session = await bot_loader.database_manager.get_session()
    
    session.add(channel_data)
    await session.commit()
    await session.refresh(channel_data)
    await session.close()
    
    return channel_data


async def get_channel(id: int) -> Channel | None:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(Channel).where(Channel.id == id)
    result = await session.exec(statement)
    
    channel = result.one_or_none()
    await session.close()
    
    return channel


async def get_channel_by_user_and_channel_id(channel_id: int, user_id: int) -> Channel | None:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(Channel).where(Channel.channel_id == channel_id).where(Channel.added_by == user_id)
    result = await session.exec(statement)
    
    channel = result.one_or_none()
    await session.close()
    
    return channel    


async def update_channel(channel_data: Channel) -> Channel:
    session = await bot_loader.database_manager.get_session()
    
    session.add(channel_data)
    await session.commit()
    await session.close()
    
    return channel_data


async def autoupdate_channel_title(channel_id: int, new_title: str):
    session = await bot_loader.database_manager.get_session()
    
    statement = update(Channel).where(Channel.channel_id == channel_id).values(title=new_title)
    await session.exec(statement)
    await session.commit()
    
    await session.close()


async def delete_channel(channel_id: int):
    session = await bot_loader.database_manager.get_session()
    
    statement = delete(Channel).where(Channel.id == channel_id)
    await session.exec(statement)
    
    await session.commit()
    await session.close()
    

async def all_channels(only_active: bool=True, user_id: int = None) -> list[Channel]:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(Channel)
    if only_active:
        statement = statement.where(Channel.active)
    if user_id:
        statement = statement.where(Channel.added_by == user_id)
    
    result = await session.exec(statement)
    await session.close()
    
    channels = result.all()
    
    return channels
