#!/usr/bin/env python3

#import hashlib

from google.protobuf.json_format import MessageToDict
from .flipperzero_protobuf_compiled import storage_pb2
from .flipper_base import cmdException

# pylint: disable=line-too-long, no-member

__all__ = [ 'FlipperProtoStorage' ]

class FlipperProtoStorage():


    # BackupRestore
    # BackupCreate
    def cmd_read(self, path=None):
        """ read file from flipperzero device

        Parameters
        ----------
        path : str
            path to file on flipper device

        Returns
        -------
            bytes

        Raises
        ----------
            cmdException

        """
        print(f"\ncmd_read path={path}")
        storage_response = []
        cmd_data = storage_pb2.ReadRequest()
        cmd_data.path = path

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_read_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")


        storage_response.append( rep_data.storage_read_response.file.data)


        # j = 0
        while rep_data.has_next:
            # j += 1
            rep_data = self._cmd_read_answer()
            storage_response.append( rep_data.storage_read_response.file.data)

        return b''.join(storage_response)

    def cmd_write(self, path=None, data=""):
        """ write file from flipperzero device

        Parameters
        ----------
        path : str
            path to file on flipper device
        data : bytes
            data to write

        Raises
        ----------
            cmdException

        """
        if self._debug:
            print(f"\ncmd_write path={path}")
        cmd_data = storage_pb2.WriteRequest()
        cmd_data.path = path

        if isinstance(data, str):
            cmd_data.file.data = data.encode()
        else:
            cmd_data.file.data = data

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_write_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")

        return rep_data.command_status

    def cmd_info(self, path=None):
        """ get filesystem info

        Parameters
        ----------
        path : str
            path to filesystem

        Returns:
        ----------
        dict

        Raises
        ----------
            cmdException

        """

        if path is None:
            raise ValueError("path can not be None")

        if self._debug:
            print(f"\ncmd_info path={path}")

        cmd_data = storage_pb2.InfoRequest()
        cmd_data.path = path

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_info_request')


        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")

        return MessageToDict(message=rep_data.storage_info_response)

    def cmd_stat(self, path=None):
        """ get info or file or directory file from flipperzero device

        Parameters
        ----------
        path : str
            path to file on flipper device

        Raises
        ----------
            cmdException

        """
        if path is None:
            raise ValueError("path can not be None")

        cmd_data = storage_pb2.StatRequest()
        cmd_data.path = path

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_stat_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")

        return MessageToDict(message=rep_data.storage_stat_response.file)

    def cmd_md5sum(self, path=None):
        """ get md5 of file

        Parameters
        ----------
        path : str
            path to file on flipper device

        Raises
        ----------
            cmdException

        """
        if self._debug:
            print(f"\ncmd_md5sum path={path}")

        cmd_data = storage_pb2.Md5sumRequest()
        cmd_data.path = path

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_md5sum_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")

        return rep_data.storage_md5sum_response.md5sum

    def cmd_mkdir(self, path=None):
        """ creates a new directory

        Parameters
        ----------
        path : str
            path for ew directory on flipper device

        Raises
        ----------
            cmdException

        """

        if self._debug:
            print(f"\ncmd_mkdir path={path}")

        cmd_data = storage_pb2.MkdirRequest()
        cmd_data.path = path

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_mkdir_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")


        return rep_data.command_status


    def cmd_delete(self, path=None, recursive=False):
        """ delete file or dir

        Parameters
        ----------
        path : str
            path to file or dir on flipper device

        Raises
        ----------
            cmdException

        """

        if self._debug:
            print(f"\ncmd_delete path={path} recursive={recursive}")

        if path is None:
            raise ValueError("path can not be None")

        cmd_data = storage_pb2.DeleteRequest()

        cmd_data.path = path
        cmd_data.recursive = recursive

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_delete_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.values_by_number[rep_data.command_status].name} path={path}")

        return rep_data.command_status

    def cmd_rename_file(self, old_path=None, new_path=None):
        """ rename file or dir

        Parameters
        ----------
        old_path : str
            path to file or dir on flipper device
        new_path : str
            path to file or dir on flipper device

        Raises
        ----------
            cmdException

        """

        if self._debug:
            print(f"\ncmd_rename_file old_path={old_path} new_path={new_path}")

        cmd_data = storage_pb2.RenameRequest()
        cmd_data.old_path = old_path
        cmd_data.new_path = new_path
        #pprint.pprint(MessageToDict(message=cmd_data, including_default_value_fields=True))

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_rename_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        return rep_data.command_status

    def cmd_storage_list(self, data="/ext"):
        """ get file & dir listing

        Parameters
        ----------
        path : str
            path to filesystem

        Returns:
        ----------
        list

        Raises
        ----------
            cmdException

        """
        # print("f_code.co_name", sys._getframe().f_code.co_name)
        storage_response = []
        cmd_data = storage_pb2.ListRequest()

        cmd_data.path = data
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'storage_list_request', has_next=True)

        if self._debug > 3:
            for i in rep_data.storage_list_response.file:
                print(type(i))
                # print(dir(i))
                print('>>', i.name, i.type, i.size)
                print('+>', i.SerializeToString())



        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        storage_response.extend(MessageToDict(message=rep_data.storage_list_response, including_default_value_fields=True)['file'])

        # print("rep_data.has_next:", rep_data.has_next)

        while rep_data.has_next:
            rep_data = self._cmd_read_answer()
            storage_response.extend(MessageToDict(message=rep_data.storage_list_response, including_default_value_fields=True)['file'])


        # return sorted(storage_response, key = lambda x: (x['type'], x['name'].lower() ))
        return storage_response
