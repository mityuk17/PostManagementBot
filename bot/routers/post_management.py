from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram.fsm.context import FSMContext
from database.crud.channel import get_channel
from database.crud.user import get_user
from database.crud.post import get_post, update_post, all_posts, delete_post
from schemas import UserRole
from texts import general_texts
from services.post_management import post_preview, cancel_posting
from keyboards import GeneralInlineKeyboard


router = Router(name="PostManagement")
    

@router.inline_query(F.query.startswith("Посты"))
async def list_posts(query: InlineQuery):
    user = await get_user(query.from_user.id)
    posts = await all_posts(
        user_id= user.id if user.role != UserRole.Admin else None,
        channel_id=int(query.query.split()[-1]) if len(query.query.split()) > 1 else None
    )
    
    response = []
    
    offset = int(query.offset) if query.offset else 0
    
    for post in posts[offset:offset+50]:
        channel = await get_channel(post.target_channel_id)
        description = f"""Дата отправки: {post.post_datetime}
Автоудаление: {post.delete_datetime if post.delete_datetime else "❌"}
Канал: {channel.title}"""
        title = f"Пост {post.id}"
        response.append(InlineQueryResultArticle(
            id=str(post.id),
            title=title,
            input_message_content=InputTextMessageContent(message_text=f"/post {post.id}"),
            description=description
        ))
    
    await query.answer(
        results=response,
        cache_time=5,
        is_personal=True,
        next_offset=str(offset+50)
    )
    

@router.message(F.text.startswith("/post "))
async def show_channel(message: Message):
    post_id = int(message.text.split()[-1])
    post = await get_post(post_id)
    user = await get_user(message.from_user.id)
    if not((user.role == UserRole.Admin) or (user.id == post.created_by)):
        return
    
    channel = await get_channel(post.target_channel_id)
    
    await message.reply(
        text=general_texts.post_info(post, channel),
        reply_markup=GeneralInlineKeyboard.post_actions(post_id, autodelete=bool(post.delete_datetime), send_without_notfication=post.send_without_notification)
    )


@router.callback_query(F.data.startswith("post-preview_"))
async def show_post_preview(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    post_id = int(callback.data.split("_")[-1])
    post = await get_post(post_id)
    
    if not post:
        return
    
    await post_preview(post)
    

@router.callback_query(F.data.startswith("switch-send-without-notification_"))
async def switch_send_without_notification(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    post_id = int(callback.data.split("_")[-1])
    post = await get_post(post_id)
    
    if not post:
        return
    channel = await get_channel(post.target_channel_id)
    post.send_without_notification = not post.send_without_notification
    await update_post(post)
    

    await callback.message.edit_text(
        text=general_texts.post_info(post, channel),
        reply_markup=GeneralInlineKeyboard.post_actions(post_id, autodelete=bool(post.delete_datetime), send_without_notfication=post.send_without_notification)
    )
    

@router.callback_query(F.data.startswith("cancel-autodelete_"))
async def cancel_autodelete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    post_id = int(callback.data.split("_")[-1])
    post = await get_post(post_id)
    
    if not post:
        return
    post.delete_datetime = None
    await update_post(post)
    channel = await get_channel(post.target_channel_id)
    
    await callback.message.edit_text(
        text=general_texts.post_info(post, channel),
        reply_markup=GeneralInlineKeyboard.post_actions(post_id, autodelete=bool(post.delete_datetime), send_without_notfication=post.send_without_notification)
    )
    

@router.callback_query(F.data.startswith("remove-post_"))
async def remove_post(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    post_id = int(callback.data.split("_")[-1])
    await delete_post(post_id)
    await cancel_posting(post_id)
    
    await callback.message.edit_text(
        text=general_texts.post_removed(),
        reply_markup=GeneralInlineKeyboard.back()
    )