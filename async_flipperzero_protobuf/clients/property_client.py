from exceptions.base_exceptions import FlipperValidateException
from commands.property_commands import PropertyGetRequestCommand
from clients.base_client import FlipperBaseProtoClient


class FlipperPropertyProtoClient(FlipperBaseProtoClient):
    async def property_get_request(self, key: str, wait_for_response: bool = True):
        stream = self.stream(PropertyGetRequestCommand(key=key))

        response = await stream.__anext__()

        if response.command_status != 0:
            raise FlipperValidateException(
                f'Command status is not equal to 0, given command: {response.command_status}'
            )

        result = [(response.property_get_response.key, response.property_get_response.value)]

        while response.has_next:
            response = await stream.__anext__()
            result.append((response.property_get_response.key, response.property_get_response.value))

        return result
