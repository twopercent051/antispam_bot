from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdding(StatesGroup):
    adding = State()

class FSMDeleting(StatesGroup):
    deleting = State()
