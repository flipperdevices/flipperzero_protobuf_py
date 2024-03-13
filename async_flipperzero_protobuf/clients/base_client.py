from exceptions.base_exceptions import FlipperValidateException
from commands.base_command import BaseCommand


class FlipperBaseProtoClient:
    def __init__(self, executor):
        self.executor = executor

    async def stream(self, command: BaseCommand):
        return await self.executor.execute_command(command=command)

    async def request(self, command: BaseCommand, wait_for_response: bool = True, to_validate: bool = True):
        response = await self.executor.execute_command(command=command)

        if not wait_for_response:
            return

        async for data in response:
            if to_validate and data.command_status != 0:
                raise FlipperValidateException(
                    f'Command status is not equal to 0, given command: {data.command_status}'
                )

            return data
