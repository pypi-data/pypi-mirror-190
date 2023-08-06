import json
from aio_pika import Message
from eon_rabbit_client.channel_controller import ChannelController


class PublishController():
    def __init__(self, channel_controller: ChannelController):
        self._channel_controller = channel_controller

    async def publish(self, body, exchange_name, routing_key):
        channel = await self._channel_controller.get_channel()
        exchange = await channel.get_exchange(exchange_name)
        message = Message(body=json.dumps(body).encode("utf-8"))
        await exchange.publish(message, routing_key=routing_key)
