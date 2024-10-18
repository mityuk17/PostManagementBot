from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas import Post


def menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Новый пост", callback_data="new-post")
    kb.button(text="Каналы", callback_data="channels")
    kb.button(text="Посты", switch_inline_query_current_chat="Посты")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def channels_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Новый канал", callback_data="new-channel")
    kb.button(text="Подключённые каналы", switch_inline_query_current_chat="Каналы")
    kb.button(text="Назад", callback_data="menu")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def channel_actions(channel_id: int, is_active: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    text = "Отключить" if is_active else "Включить"
    kb.button(text=text, callback_data=f"switch-channel_{channel_id}")
    kb.button(text="Запланированные посты", switch_inline_query_current_chat=f"Посты {channel_id}")
    kb.button(text="Удалить", callback_data=f"remove-channel_{channel_id}")
    
    kb.adjust(1, repeat=True)
    return kb.as_markup()


def post_actions(post_id: int, autodelete: bool, send_without_notfication: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Превью", callback_data=f"post-preview_{post_id}")
    
    if send_without_notfication:
        kb.button(text="🔕Без уведомления", callback_data=f"switch-send-without-notification_{post_id}")
    else:
        kb.button(text="🔔С уведомлением", callback_data=f"switch-send-without-notification_{post_id}")
        
    if autodelete:
        kb.button(text="Отменить автоудаление", callback_data=f"cancel-autodelete_{post_id}")
        
    kb.button(text="Удалить", callback_data=f"remove-post_{post_id}")
    kb.button(text="Назад", callback_data="menu")
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()

def back(callback_data: str = "menu") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="↩️Назад", callback_data=callback_data)
    
    return kb.as_markup()


def cancel(callback_data: str = "menu") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="❌Отмена", callback_data=callback_data)
    
    return kb.as_markup()


def post_button(post_data: Post):
    kb = InlineKeyboardBuilder()
    if not post_data.button_label:
        return
    
    if post_data.button_url:
        kb.button(text=post_data.button_label, url=post_data.button_url)
    elif post_data.button_subscribed_text and post_data.button_unsubscribed_text:
        kb.button(text=post_data.button_label, callback_data=f"""check-subscription_{post_data.id if post_data.id else "preview"}""")
        
    return kb.as_markup()