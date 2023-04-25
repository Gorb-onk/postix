from abc import abstractmethod, ABC


class BasePublisher(ABC):
    async def __aenter__(self):
        return self

    @abstractmethod
    async def send(self, chat_id: str, text: str) -> None:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
