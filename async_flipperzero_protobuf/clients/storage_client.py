from google.protobuf.json_format import MessageToDict
from commands.storage_commands import (
    StorageBackupRestoreRequestCommand,
    StorageBackupCreateRequestCommand,
    StorageTimestampRequestCommand,
    StorageRenameRequestCommand,
    StorageMd5sumRequestCommand,
    StorageDeleteRequestCommand,
    StorageStartRequestCommand,
    StorageMkdirRequestCommand,
    StorageStatRequestCommand,
    StorageInfoRequestCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperStorageProtoClient(FlipperBaseProtoClient):
    async def storage_backup_create_request(self, archive_path: str, wait_for_response: bool = True):
        return await self.request(
            StorageBackupCreateRequestCommand(archive_path=archive_path),
            wait_for_response=wait_for_response,
            to_validate=True,
        )

    async def storage_backup_restore_request(self, archive_path: str, wait_for_response: bool = True):
        return await self.request(
            StorageBackupRestoreRequestCommand(archive_path=archive_path),
            wait_for_response=wait_for_response,
            to_validate=True,
        )

    async def storage_read_request(self):
        raise NotImplementedError()  # TODO: implement

    async def storage_write_request(self):
        raise NotImplementedError()  # TODO: implement

    async def storage_info_request(self, path: str, wait_for_response: bool = True):
        response = await self.request(
            StorageInfoRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )
        return MessageToDict(message=response.storage_info_response)

    async def storage_start_request(self, path: str, wait_for_response: bool = True):
        response = await self.request(
            StorageStartRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )
        return MessageToDict(
            message=response.storage_stat_response.file,
            including_default_value_fields=True,
        )

    async def storage_timestamp_request(self, path: str, wait_for_response: bool = True):
        response = await self.request(
            StorageTimestampRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )
        return response.storage_timestamp_response.timestamp

    async def storage_stat_request(self, path: str, wait_for_response: bool = True):
        response = await self.request(
            StorageStatRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )
        return MessageToDict(
            message=response.storage_stat_response.file,
            including_default_value_fields=True,
        )

    async def storage_md5sum_request(self, path: str, wait_for_response: bool = True):
        response = await self.request(
            StorageMd5sumRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )
        return response.storage_md5sum_response.md5sum

    async def storage_mkdir_request(self, path: str, wait_for_response: bool = True):
        return await self.request(
            StorageMkdirRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )

    async def storage_delete_request(self, path: str, recursive: bool = False, wait_for_response: bool = True):
        return await self.request(
            StorageDeleteRequestCommand(path=path, recursive=recursive),
            wait_for_response=wait_for_response,
            to_validate=True,
        )

    async def storage_rename_request(self, old_path: str, new_path: str, wait_for_response: bool = True):
        return await self.request(
            StorageRenameRequestCommand(old_path=old_path, new_path=new_path),
            wait_for_response=wait_for_response,
            to_validate=True,
        )

    async def storage_list_request(self, old_path: str, new_path: str, wait_for_response: bool = True):
        raise NotImplementedError()  # TODO: implement
