from aiogram.fsm.state import State, StatesGroup


class PostCreation(StatesGroup):
    channel_id = State()
    messages = State()
    button_type = State()
    button_label = State()
    button_url = State()
    button_subscribed_text = State()
    button_unsubscribed_text = State()
    send_without_notification = State()
    post_datetime = State()
    delete_datetime = State()
    preview_check = State()
