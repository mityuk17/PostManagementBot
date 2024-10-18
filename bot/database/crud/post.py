from botloader import bot_loader
from schemas import Post
from sqlmodel import select, delete
from datetime import datetime


async def create_post(post_data: Post) -> Post:
    session = await bot_loader.database_manager.get_session()
    
    session.add(post_data)
    await session.commit()
    await session.refresh(post_data)
    await session.close()
    
    return post_data


async def get_post(post_id: int) -> Post | None:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(Post).where(Post.id == post_id)
    result = await session.exec(statement)
    post = result.one_or_none()
    await session.close()
    
    return post


async def update_post(post_data: Post) -> Post:
    session = await bot_loader.database_manager.get_session()
    
    session.add(post_data)
    await session.commit()
    await session.close()
    
    return post_data


async def delete_post(post_id: int):
    session = await bot_loader.database_manager.get_session()
    
    statement = delete(Post).where(Post.id == post_id)
    await session.exec(statement)
    
    await session.commit()
    await session.close()


async def all_posts(relevant: bool = True, user_id: int = None, channel_id: int = None) -> list[Post]:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(Post)
    if relevant:
        statement = statement.where(Post.post_datetime > datetime.today())
    if user_id:
        statement = statement.where(Post.created_by == user_id)
    if channel_id:
        statement = statement.where(Post.target_channel_id == channel_id)
        
    statement = statement.order_by(Post.post_datetime)
    
    result = await session.exec(statement)
    posts = result.all()
    
    return posts
