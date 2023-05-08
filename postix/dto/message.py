from dataclasses import dataclass, field


@dataclass
class Message:
    text: str
    photos: list[bytes] = field(default_factory=list)

