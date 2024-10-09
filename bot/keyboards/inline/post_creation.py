from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas import Channel


def pick_target_channel(channels: list[Channel]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    for channel in channels:
        kb.button(text=channel.title, callback_data=f"channel-id_{channel.id}")
    
    kb.button(text="❌Отмена", callback_data="menu")
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def pick_button_type() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Проверка на подписку", callback_data="button-type_check-subscription")
    kb.button(text="Ссылка", callback_data="button-type_url")
    kb.button(text="Без кнопки", callback_data="button-type_no")
    kb.button(text="❌Отмена", callback_data="menu")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def pick_without_notification() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔔Со звуком", callback_data="without-notification_no")
    kb.button(text="🔕Без звука", callback_data="without-notification_yes")
    kb.button(text="❌Отмена", callback_data="menu")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def pick_delete_datetime() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for t in [1, 6, 12, 24, 48, 72]:
        kb.button(text=f"{t}ч.", callback_data="delete-datetime_{t}")
    kb.button(text="Без удаления", callback_data="delete-datetime_no")
    kb.button(text="❌Отмена", callback_data="menu")
    
    kb.adjust(3, 3, 1, 1)
    
    return kb.as_markup()


def preview_check() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅Сохранить пост", callback_data="save-post")
    kb.button(text="❌Удалить пост", callback_data="cancel-post")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()