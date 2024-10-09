from html import escape


def get_channel_id() -> str:
    text = "Перешлите сообщение из канала, который хотите добавить или пришлите <i>channel_id</i>"
    
    return text


def channel_already_exists() -> str:
    text = "Данный канал уже подключен"
    
    return text


def channel_not_found() -> str:
    text = "Бот не нашёл канал. Проверьте, что бот добавлен в канал с правами администратора"
    
    return text


def channel_created(title: str) -> str:
    text = f"Канал {title} успешно подключен"
    
    return text


def invalid_channel_id() -> str:
    text = "❗️Сообщение должно быть переслано из канала или в нём должен быть <i>channel_id</i>"
    
    return text


def not_channel_admin() -> str:
    text = "❗️Вы не являетесь админом канала"
    
    return text