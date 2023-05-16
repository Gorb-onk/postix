import asyncio
from asyncio import Queue
from datetime import datetime
from random import randint
from unittest.mock import AsyncMock

import pytest
from telethon.tl.types import Photo, PhotoSize, MessageMediaPhoto

from postix.config import caches
from telethon import events, types

from postix.dto import Message
from postix.observers import TelegramObserver


async def check_queue(queue: Queue, expected_messages: list[Message]) -> None:
    for expected_message in expected_messages:
        msg = await queue.get()
        assert msg == expected_message
    assert queue.empty()


def build_message(channel_id: int, text: str, media: bytes | None = None, **kwargs) -> events.NewMessage:
    if media:
        photo = Photo(id=randint(1, 1000000), access_hash=randint(1, 1000000), file_reference=media, date=datetime.now(),
                      sizes=[PhotoSize('a', 10, 10, 10)], dc_id=randint(1, 1000000))
    else:
        photo = None
    msg = types.Message(id=randint(1, 100000), peer_id=types.PeerChannel(channel_id=channel_id), date=datetime.now(),
                        message=text, media=MessageMediaPhoto(photo=photo))
    return events.NewMessage.build(types.UpdateNewMessage(msg, 1, 2))


async def add_messages(msgs: list[events.NewMessage], observer: TelegramObserver) -> None:
    for msg in msgs:
        msg._set_client(observer.client)
        await observer.client._dispatch_event(msg)


@pytest.mark.asyncio
async def test_text_msg(mocker):
    mocker.patch('postix.observers.telegram.TelegramClient.start', side_effect=AsyncMock())
    mocker.patch('postix.observers.telegram.TelegramClient.run_until_disconnected', side_effect=AsyncMock())

    queue = Queue()
    observer = TelegramObserver(queue, 'test', 1, '1', cache=caches.get('test'))

    channel_id = 123
    msg_text = '123'

    original_message = build_message(channel_id, msg_text)
    expected_message = Message(msg_text, [])

    tasks = asyncio.gather(observer.run([channel_id]),
                           check_queue(queue, [expected_message]),
                           add_messages([original_message], observer))

    await asyncio.wait_for(tasks, timeout=5)


@pytest.mark.asyncio
async def test_text_with_photo_msg(mocker):
    mocker.patch('postix.observers.telegram.TelegramClient.start', side_effect=AsyncMock())
    mocker.patch('postix.observers.telegram.TelegramClient.run_until_disconnected', side_effect=AsyncMock())

    queue = Queue()
    observer = TelegramObserver(queue, 'test', 1, '1', cache=caches.get('test'))

    channel_id = 123
    msg_text = '123'
    photo = b'test_photo_bytes_data' * 512

    original_message = build_message(channel_id, msg_text, media=photo)
    expected_message = Message(msg_text, [photo])

    tasks = asyncio.gather(observer.run([channel_id]),
                           check_queue(queue, [expected_message]),
                           add_messages([original_message], observer))

    await asyncio.wait_for(tasks, timeout=50)

