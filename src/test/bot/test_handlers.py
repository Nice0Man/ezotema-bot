from unittest.mock import AsyncMock, patch
import pytest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.handlers.start import start_handler


class TestStartHandler:

    @pytest.mark.asyncio
    async def test_start_handler_triggered(self, mocker):
        message = mocker.Mock(spec=Message)
        state = mocker.Mock(spec=FSMContext)
        state.set_state = AsyncMock()
        message.answer_photo = AsyncMock()

        with patch(
            "src.main.bot.handlers.start.render_template", return_value="Welcome!"
        ):
            with patch(
                "src.main.bot.handlers.start.setup_start_keyboard",
                return_value=AsyncMock(),
            ):
                await start_handler(message, state)

        state.set_state.assert_called_once_with(CourseStates.START)
        message.answer_photo.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_handler_already_in_start_state(self, mocker):
        message = mocker.Mock(spec=Message)
        state = mocker.Mock(spec=FSMContext)
        state.set_state = AsyncMock()
        state.get_state = AsyncMock(return_value=CourseStates.START)
        message.answer_photo = AsyncMock()

        with patch(
            "src.main.bot.handlers.start.render_template", return_value="Welcome!"
        ):
            with patch(
                "src.main.bot.handlers.start.setup_start_keyboard",
                return_value=AsyncMock(),
            ):
                await start_handler(message, state)

        state.set_state.assert_called_once_with(CourseStates.START)
        message.answer_photo.assert_called_once()
