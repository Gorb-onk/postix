import config
from publishers import BasePublisher, TelegramPublisher


class MessageProcessor:
    def __init__(self, publisher: BasePublisher, target_channels: list[str]):
        self.channels = target_channels
        self.publisher = publisher

    async def process(self, msg: str) -> None:
        async with TelegramPublisher(config.TELEGRAM_BOT_TOKEN) as tg_publisher:
            for channel in self.channels:
                await tg_publisher.send(channel, msg)
