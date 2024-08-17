from aiogram.fsm.state import State, StatesGroup


# FSM States
class CourseStates(StatesGroup):
    START = State()
    IDLE = State()
    STEP_1 = State()
    STEP_2 = State()
    STEP_3 = State()
    STEP_4 = State()
    STEP_5 = State()
    STEP_6 = State()
    STEP_7 = State()
    STEP_8 = State()
    STEP_9 = State()
    STEP_10 = State()
