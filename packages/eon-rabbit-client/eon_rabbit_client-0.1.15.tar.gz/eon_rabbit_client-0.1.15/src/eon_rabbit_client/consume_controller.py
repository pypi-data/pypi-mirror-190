from inspect import iscoroutinefunction as isAsync
import json
from aio_pika import IncomingMessage
from eon_rabbit_client.channel_controller import ChannelController


async def await_if_async(func, *args):
    if func:
        await func(*args) if isAsync(func) else func(*args)


def body_to_json(messageArgs):
    try:
        messageArgs["body"] = messageArgs["body"].decode()
        messageArgs["body"] = json.loads(messageArgs["body"])

    except json.decoder.JSONDecodeError as e:
        body = messageArgs["body"]
        raise Exception(f"({body}) is not a valid JSON")


def create_handler(
    handler,
    on_success,
    on_error,
    after_all,
):
    async def message_handler(message: IncomingMessage):
        messageArgs = {
            "body": message.body,
            "routing_key": message.routing_key,
            "exchange": message.exchange,
        }
        try:
            body_to_json(messageArgs)
            await await_if_async(handler, messageArgs)
            await await_if_async(on_success, messageArgs)
            await message.ack()

        except Exception as error:
            await await_if_async(on_error, messageArgs, error)
            await message.nack(requeue=False)

        finally:
            await await_if_async(after_all, messageArgs)

    return message_handler


class ConsumeController:
    def __init__(self, channel_controller: ChannelController):
        self.channel_controller = channel_controller

    async def consume(
        self,
        queue_name,
        handler,
        on_success=None,
        on_error=None,
        after_all=None,
    ):
        channel = await self.channel_controller.get_channel()
        queue = await channel.get_queue(queue_name)
        
        print(f"Consuming: {queue_name}")
        message_handler = create_handler(
            handler,
            on_success,
            on_error,
            after_all,
        )

        return await queue.consume(message_handler)
