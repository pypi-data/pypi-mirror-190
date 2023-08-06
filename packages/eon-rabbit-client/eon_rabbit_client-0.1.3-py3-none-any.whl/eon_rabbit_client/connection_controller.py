from aio_pika import connect_robust, RobustConnection


class ConnectionController:
    def __init__(self, host, port, user, password, name):
        self._name = name
        self._host = host
        self._port = port
        self._user = user
        self._connection = None
        self._password = password
        self._connection_string = f"amqp://{user}:{password}@{host}/?name={name}"

    async def get_connection(self) -> RobustConnection:
        if not self._connection:
            await self._connect()
        return self._connection

    async def _connect(self) -> None:
        self._log("connecting")
        self._connection = connect_robust(self._connection_string)
        self._connection = await self._connection
        self._log("connected")
        self._set_connection_callbacks()

    def _set_connection_callbacks(self):
        self._connection.close_callbacks.add(self._on_close)
        self._connection.reconnect_callbacks.add(self._on_reconnect)

    def _on_close(self, connection, reason):
        self._log("connection closed")

    def _on_reconnect(self, connection):
        self._log("reconnected")

    def _log(self, content):
        prefix = f"RabbitMQ connection({self._host})"
        print(f"{prefix}: {content}")
