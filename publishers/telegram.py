from aiogram import Bot


class TelegramPublisher:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def __aenter__(self):
        return self

    async def send(self, chat_id: str, text: str) -> None:
        await self.bot.send_message(chat_id, text)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        session = await self.bot.get_session()
        await session.close()
