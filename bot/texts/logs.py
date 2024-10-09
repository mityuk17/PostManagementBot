from html import escape
from schemas import Post, Channel


def post_publication(post_data: Post) -> str:
    text = f"Пост {post_data.id}: создан {post_data.created_by}. Отправка {post_data.post_datetime};"
    if post_data.delete_datetime:
        text += f"Удаление {post_data.delete_datetime}"
    else:
        text += f"Без удаления"
        
    return text


def post_deleted(post_data: Post) -> str:
    text = f"Пост {post_data.id} "
    if post_data.deleted:
        text += "автоматически удалён"
    else:
        text += "требует ручного удаления"
    
    return text


def post_cancelled(post_data: Post) -> str:
    text = f"Пост {post_data.id} отменён пользователем {post_data.created_by}"
    
    return text


def post_not_found(post_id: int) -> str:
    text = f"Пост {post_id} не найден"

    return text

def channel_added(channel_data: Channel) -> str:
    text = f"Канал {channel_data.id} ({channel_data.channel_id}) создан {channel_data.added_by}"
    
    return text


def channel_removed(channel_data: Channel) -> str:
    text = f"Канал {channel_data.id} ({channel_data.channel_id}) удалён пользователем {channel_data.added_by}"
    
    return text


def channel_not_found(channel_id: int) -> str:
    text = f"Канал {channel_id} не найден"
    
    return text


def no_messages_copied(post_data: Post) -> str:
    text = f"Пост {post_data.id}. Сообщения для копирования от пользователя {post_data.created_by} не найдены"
    
    return text