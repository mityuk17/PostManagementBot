from html import escape
from schemas import Post, Channel


def menu() -> str:
    text = "<b>Меню</b>"
    
    return menu


def post_info(post: Post, channel: Channel) -> str:
    text = f"""Пост {post.id}
Канал: {escape(channel.title)} ({channel.id})
Дата отправки: {post.post_datetime}
Дата удаления: {post.delete_datetime}"""

    if post.send_without_notification:
        text += "\n🔕Отправка без звука"

    return text


def channel_info(channel: Channel, for_admin: bool = False) -> str:
    text = f"""Канал {channel.id}
Название: {escape(channel.title)}
Channel_id: {channel.channel_id}
Статус: {"✅Активен" if channel.active else "❌Отключён"}"""

    if for_admin:
        text += f"\nДобавлен пользователем {channel.added_by}"

    return text


def channel_removed() -> str:
    text = "Канал удалён"
    
    return text


def post_removed() -> str:
    text = "Пост удалён"
    
    return text