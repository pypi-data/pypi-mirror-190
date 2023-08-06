from eon_rabbit_client.channel_controller import ChannelController

class ExchangeController():
    def __init__(self, channel_controller: ChannelController):
        self._channel_controller = channel_controller

    async def create_exchange(self, name, type):
        channel = await self._channel_controller.get_channel()
        return await channel.declare_exchange(name, type, durable=True)
