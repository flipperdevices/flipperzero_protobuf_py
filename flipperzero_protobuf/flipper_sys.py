#!/usr/bin/env python3

# import sys
# import os
import datetime
# import pprint

# from nis import match
# from numpy import mat

# pylint: disable=line-too-long, no-member

from google.protobuf.json_format import MessageToDict
from .flipperzero_protobuf_compiled import system_pb2, flipper_pb2
from .flipper_base import cmdException, InputTypeException

__all__ = ['FlipperProtoSys']


class FlipperProtoSys:

    # FactoryReset
    def rpc_factory_reset(self):
        """ Factory Reset

        Parameters
        ----------
        None

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """

        cmd_data = system_pb2.FactoryResetRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_factory_reset_request')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # Update
    def rpc_update(self, update_manifest=""):
        """ Update

        Parameters
        ----------
        update_manifest : str

        Returns
        ----------
        code ; str
            0 OK
            1 ManifestPathInvalid
            2 ManifestFolderNotFound
            3 ManifestInvalid
            4 StageMissing
            5 StageIntegrityError
            6 ManifestPointerError
            7 TargetMismatch
            8 OutdatedManifestVersion
            9 IntFull

        """
        cmd_data = system_pb2.UpdateRequest()
        cmd_data.update_manifest = update_manifest

        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_update_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.Status_values_by_number[rep_data.command_status].name} update_manifest={update_manifest}")

    # Reboot
    def rpc_reboot(self, mode=0):
        """ Reboot flipper

        Parameters
        ----------
        mode : int or str
            0 = OS
            1 = DFU
            2 = UPDATE

        Raises
        ----------
        InputTypeException
        cmdException

        """
        # pylint: disable=broad-except
        cmd_data = system_pb2.RebootRequest()

        if mode not in ['OS', 'DFU', 'UPDATE']:
            raise InputTypeException("Invalid Reboot mode")
        cmd_data.mode = getattr(cmd_data, mode)

        try:

            # nothing happens if only cmd_send is called and response is not read
            # rep_data = self._rpc_send(cmd_data, 'system_reboot_request')

            # gets SerialException from attempt to read response
            rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_reboot_request')
        # except serial.serialutil.SerialException as _e:
        except Exception as _e:
            return

        # we should not get here
        if rep_data.command_status != 0:
            raise cmdException(f"{self.Status_values_by_number[rep_data.command_status].name} mode={mode}")

    # PowerInfo
    def rpc_power_info(self):
        """ Power info / charging status

        Parameters
        ----------
        None

        Returns
        ----------
        key, value : str

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.PowerInfoRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_power_info_request')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

        return rep_data.system_power_info_response.key, rep_data.system_power_info_response.value

    # DeviceInfo
    def rpc_device_info(self):
        """ Device Info

        Return
        ----------
        key, value : str

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.DeviceInfoRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_device_info_request')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

        return rep_data.system_device_info_response.key, rep_data.system_device_info_response.value

    # ProtobufVersion
    def rpc_protobuf_version(self):
        """ Protobuf Version

        Parameters
        ----------
        None

        Return
        ----------
        major, minor : int

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.ProtobufVersionRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_protobuf_version_request')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

        return rep_data.system_protobuf_version_response.major, rep_data.system_protobuf_version_response.minor

    # GetDateTime
    def rpc_get_datetime(self):
        """ Get system Date and Time

        Parameters
        ----------
        None

        Returns
        ----------
        dict
            keys: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.GetDateTimeRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_get_datetime_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)
        return MessageToDict(rep_data.system_get_datetime_response)['datetime']

    # SetDateTime
    def rpc_set_datetime(self, arg_datetm=None):
        """ Set system Date and Time

        Parameters
        ----------
        datetm : dict or datetime obj
            dict keys: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'
            datetime obj
            None (default) method datetime.datetime.now() is called

        Returns
        ----------
        None

        Raises
        ----------
        InputTypeException
        cmdException

        """
        if arg_datetm is None:
            datetm = datetime.datetime.now()
        else:
            datetm = arg_datetm

        cmd_data = system_pb2.SetDateTimeRequest()

        if isinstance(datetm, datetime.datetime):
            cmd_data.datetime.year = datetm.year
            cmd_data.datetime.month = datetm.month
            cmd_data.datetime.day = datetm.day
            cmd_data.datetime.hour = datetm.hour
            cmd_data.datetime.minute = datetm.minute
            cmd_data.datetime.second = datetm.second
            cmd_data.datetime.weekday = datetm.isoweekday()
        elif isinstance(datetm, dict):
            cmd_data.datetime.update(datetm)
        else:
            raise InputTypeException("Invalid datetime value")

        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_set_datetime_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.Status_values_by_number[rep_data.command_status].name} arg_datetm={arg_datetm}")

    # Ping
    def rpc_system_ping(self, data=bytes([0xde, 0xad, 0xbe, 0xef])):
        """ Ping flipper

        Parameters
        ----------
        data : bytes

        Returns
        ----------
        None

        Raises
        ----------
        InputTypeException
        cmdException

        """

        cmd_data = system_pb2.PingRequest()

        if not isinstance(data, bytes):
            raise InputTypeException("Invalid Ping data value")

        cmd_data.data = data
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'system_ping_request')

        if rep_data.command_status != 0:
            raise cmdException(f"{self.Status_values_by_number[rep_data.command_status].name} data={data}")

        return rep_data.system_ping_response.data

    # PlayAudiovisualAlert
    def rpc_audiovisual_alert(self):
        """ Launch audiovisual alert on flipper ??

        Parameters
        ----------
        None

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """

        cmd_data = system_pb2.PlayAudiovisualAlertRequest()
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, 'system_play_audiovisual_alert_request')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # pylint: disable=protected-access
    def rpc_stop_session(self):
        """ Stop RPC session

        Parameters
        ----------
        None

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """

        cmd_data = flipper_pb2.StopSession()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'stop_session')

        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

        self.flip._in_session = False
