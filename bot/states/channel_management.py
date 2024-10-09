from aiogram.fsm.state import State, StatesGroup


class ChannelCreation(StatesGroup):
    channel_id = State()