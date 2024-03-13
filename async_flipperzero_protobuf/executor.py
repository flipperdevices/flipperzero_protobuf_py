import asyncio

from flipperzero_protobuf_compiled import flipper_pb2
from connectors.base_connector import BaseConnector
from commands.base_command import BaseCommand


class FlipperProtoExecutor:
    def __init__(self, connector: BaseConnector):
        self._connector = connector
        # self.is_loop_running = False
        # self.command_queue = deque()
        self.events = {}
        self.command_id = 0

        self.runner_task = None

    async def execute_command(self, command: BaseCommand):
        self.command_id += 1

        event = asyncio.Event()
        self.events[self.command_id] = [None, event]
        waiter = self.event_waiter(self.command_id, event)

        await command.execute(command_id=self.command_id, connector=self._connector)

        return waiter

    async def event_waiter(self, event_name, event):
        while True:
            await event.wait()
            event.clear()
            # print(event_name)
            yield self.events[event_name][0]

    async def _run_command_event_loop(self):  # set cor as done
        while True:
            length = await self._connector.read_varint_32()
            data = flipper_pb2.Main()
            read_exactly = await self._connector.read_exactly(n=length)
            data.ParseFromString(read_exactly)

            # print(data)
            if event := self.events.get(data.command_id):
                # event.set_result(data)
                event[0] = data
                event[1].set()
                # print("event: ", event[1])

    async def start(self):
        self.runner_task = asyncio.create_task(self._run_command_event_loop())
        await asyncio.sleep(0)

        return self

    async def stop(self):
        if not self.runner_task.cancelled():
            self.runner_task.cancel()

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        return await self.stop()
