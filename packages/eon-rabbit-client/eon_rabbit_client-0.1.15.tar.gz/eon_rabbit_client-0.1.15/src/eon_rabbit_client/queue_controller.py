import asyncio
from eon_rabbit_client.channel_controller import ChannelController


class QueueController:
    def __init__(self, channel_controller: ChannelController, prefetch_count=None):
        self._channel_controller = channel_controller
        self._prefetch_count = prefetch_count

    async def assert_queue(self, queue_name):
        channel = await self._channel_controller.get_channel()
        await channel.declare_queue(queue_name)
        
    async def bind_queue(self, queue_name, exchange, bindingKeys):
        channel = await self._channel_controller.get_channel()
        queue = await channel.get_queue(queue_name)
        await asyncio.gather(
            *(queue.bind(exchange, bindingKey) for bindingKey in bindingKeys)
        )
