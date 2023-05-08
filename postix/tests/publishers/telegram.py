from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock, Mock

from postix.dto import Message
from postix.publishers import TelegramPublisher


class TelegramPublisherTestCase(IsolatedAsyncioTestCase):
    @patch('postix.publishers.telegram.Bot')
    def test_creation(self, bot_mock: Mock):
        token = 'test_token'
        TelegramPublisher(token)
        bot_mock.assert_called_once_with(token=token)

    @patch('postix.publishers.telegram.Bot')
    async def test_send_msg(self, bot_mock: Mock):
        bot_mock.return_value.send_message = AsyncMock()
        bot_mock.return_value.get_session = AsyncMock()

        chat_id = '1'
        msg = Message(text='msg')

        async with TelegramPublisher('test_token') as publisher:
            await publisher.send(chat_id, msg)

        bot_mock.return_value.send_message.assert_awaited_once_with(chat_id=chat_id, text=msg.text)

    @patch('postix.publishers.telegram.Bot')
    async def test_session_closed(self, bot_mock: Mock):
        bot_mock.return_value.get_session = AsyncMock()

        async with TelegramPublisher('test_token') as publisher:
            pass
        bot_mock.return_value.get_session.return_value.close.assert_awaited_once_with()
