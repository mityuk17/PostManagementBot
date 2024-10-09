from html import escape
from schemas import Post, Channel


def post_send(post_data: Post, channel: Channel) -> str:
    text = f"""Пост {post_data.id}
Канал: {escape(channel.title)} ({channel.channel_id})
Статус: ✅Отправлен {post_data.post_datetime}"""

    return text


def post_delete(post_data: Post, channel: Channel) -> str:
    if post_data.deleted:
        status = f"🗑️ Удалён {post_data.delete_datetime}"
    else:
        status = f"🚮 Необходимо удалить вручную"

    text = f"""Пост {post_data.id}
Канал {escape(channel.title)} ({channel.channel_id})
Статус: {status}"""

    return text