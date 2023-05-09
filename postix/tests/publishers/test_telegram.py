from unittest.mock import AsyncMock

import pytest

from postix.dto import Message
from postix.publishers import TelegramPublisher


@pytest.mark.asyncio
async def test_creation(mocker):
    mocked_bot = mocker.patch('postix.publishers.telegram.Bot')
    token = 'test_token'
    TelegramPublisher(token)
    mocked_bot.assert_called_once_with(token=token)


@pytest.mark.asyncio
async def test_send_msg(mocker):
    mocked_bot = mocker.patch('postix.publishers.telegram.Bot')
    mocked_bot.return_value = AsyncMock()

    chat_id = '1'
    msg = Message(text='msg')

    async with TelegramPublisher('test_token') as publisher:
        await publisher.send(chat_id, msg)

    mocked_bot.return_value.send_message.assert_awaited_once_with(chat_id=chat_id, text=msg.text)


@pytest.mark.asyncio
async def test_send_msg(mocker):
    mocked_bot = mocker.patch('postix.publishers.telegram.Bot')
    mocked_bot.return_value = AsyncMock()

    async with TelegramPublisher('test_token'):
        pass

    mocked_bot.return_value.get_session.return_value.close.assert_awaited_once_with()
