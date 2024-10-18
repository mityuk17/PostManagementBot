from html import escape


def pick_target_channel() -> str:
    text = "Выберите из списка канал, в который будет отправлен пост:"
    
    return text


def picked_target_channel(title: str) -> str:
    text = f"Канал для постинга: {escape(title)}"
    
    return text


def get_messages() -> str:
    text = "Пришлите сообщение-контент поста:"
    
    return text


def got_media_group() -> str:
    text = "❗️Получена группа медиа, добавление кнопки к посту отключено."

    return text


def pick_button_type() -> str:
    text = "Выберите тип кнопки, которая будет прикреплена к посту:"
    
    return text


def picked_button_type(button_type: str):
    match button_type:
        case "check-subscription":
            button = "Проверка подписки"
        case "url":
            button = "Ссылка"
        case "no":
            button = "Без кнопки"
            
    text = f"""Тип кнопки: {button}"""
    
    return text


def get_button_label() -> str:
    text = "Пришлите надпись, которая будет отображаться на кнопке:"

    return text


def get_button_subscribed_text() -> str:
    text = "Пришлите текст, который будет показываться, если пользователь подписан на канал:"
    
    return text


def get_button_unsubscribed_text() -> str:
    text = "Пришлите текст, который будет показывать, если пользователь <b>не</b> подписан на канал:"
    
    return text


def get_button_url() -> str:
    text = "Пришлите ссылку, которая будет вставлена в кнопку:"
    
    return text


def invalid_url() -> str:
    text = "Проверьте, что ссылка является валидной и попробуйте снова"
    
    return text


def pick_without_notification() -> str:
    text = "Отправить пост со звуком или без?"
    
    return text


def picked_without_notification(without_notification: bool) -> str:
    if without_notification:
        text = "Пост без уведомления🔕"
    else:
        text = "Пост с уведомлением🔔"
        
    return text


def get_post_datetime() -> str:
    text = """Когда должен быть опубликован пост?
Пришлите дату и время в формате <b>01.01.2024 12:00</b>"""

    return text


def invalid_post_datetime() -> str:
    text = "Проверьте правильность формата даты и времени и попробуйте снова"
    
    return text


def get_delete_hours() -> str:
    text = """Через сколько часов после публикации пост должен быть удалён?
Пришлите <b>целое число</b> часов или выберите из списка"""

    return text


def picked_delete_hours(hours: int) -> str:
    text = f"Пост будет удален через {hours} ч. после отправки."
    
    return text


def invalid_delete_hours() -> str:
    text = """Проверьте, что вы прислали целое число и попробуйте снова"""
    
    return text


def post_preview_info() -> str:
    text = "Превью поста"
    
    return text


def post_confirmation() -> str:
    text = "Создание поста завершено"
    
    return text


def post_cancelled() -> str:
    text = "Создание поста отменено"
    
    return text
