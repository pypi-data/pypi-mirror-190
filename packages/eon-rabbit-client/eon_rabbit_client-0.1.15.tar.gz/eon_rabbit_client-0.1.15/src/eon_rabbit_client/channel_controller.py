from eon_rabbit_client.connection_controller import ConnectionController
from aio_pika import RobustChannel

class ChannelController():
    def __init__(self, connection_controller: ConnectionController, prefetch_count=None):
        self._channel = None
        self._connection_controller = connection_controller
        self._prefetch_count = prefetch_count

    async def get_channel(self) -> RobustChannel:
        if not self._channel:
            await self._create_channel()
        return self._channel

    async def _create_channel(self):
        connection = await self._connection_controller.get_connection()
        self._channel = connection.channel()
        self._channel = await self._channel
        if self._prefetch_count:
            await self._channel.set_qos(prefetch_count=self._prefetch_count)
            
