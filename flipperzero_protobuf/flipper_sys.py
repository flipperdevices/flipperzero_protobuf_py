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

__all__ = [ 'FlipperProtoSys']


class FlipperProtoSys:

    # FactoryReset

    # Update
    def cmd_Update(self, update_manifest=""):
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

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_update_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        code = rep_data.system_update_response.code
        return rep_data.DESCRIPTOR.enum_types_by_name['UpdateResultCode'].values_by_number[code].name

    # Reboot
    def cmd_Repoot(self, mode=0):
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
        # mode
        cmd_data = system_pb2.RebootRequest()

        # print(dir(cmd_data))

        if mode not in ['OS', 'DFU', 'UPDATE']:
            raise InputTypeException("Invalid Reboot mode")
        cmd_data.mode = cmd_data.getattr(mode)

        # print(MessageToDict(message=cmd_data, including_default_value_fields=True))
        # data = self._cmd_send(cmd_data, 'system_reboot_request')
        try:
            self._cmd_send_and_read_answer(cmd_data, 'system_reboot_request')
        # except serial.serialutil.SerialException as _e:
        except Exception as _e:
            pass

    # PowerInfo
    def cmd_PowerInfo(self):
        """ Power info / charging status

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.PowerInfoRequest()
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_power_info_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        return rep_data.system_power_info_response
        # return MessageToDict(message=data.system_power_info_response)

    # DeviceInfo
    def cmd_DeviceInfo(self):
        """ Device Info

        Return
        ----------
        key, value : str

        Raises
        ----------
        cmdException

        """
        cmd_data = system_pb2.DeviceInfoRequest()
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_device_info_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        return rep_data.system_device_info_response.key, rep_data.system_device_info_response.value

    # ProtobufVersion
    def cmd_ProtobufVersion(self):
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
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_protobuf_version_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        return rep_data.system_protobuf_version_response.major, rep_data.system_protobuf_version_response.minor

    # GetDateTime
    def cmd_GetDateTime(self):
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
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_get_datetime_request')
        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)
        return MessageToDict(rep_data.system_get_datetime_response)['datetime']

    # SetDateTime
    def cmd_SetDateTime(self, datetm=None):
        """ Set system Date and Time

        Parameters
        ----------
        datetm : dict or datetime obj
            dict keys: 'year', 'month', 'day', 'hour', 'minute', 'second', 'weekday'
            datetime obj
            None (default) method datetime.datetime.now() is called

        Raises
        ----------
        InputTypeException
        cmdException

        """
        if datetm is None:
            datetm = datetime.datetime.now()

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

        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_set_datetime_request')
        # print("SetDateTimeRequest data", dir(data))
        # print("SetDateTimeRequest data", MessageToDict(message=data))

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

    # Ping
    def cmd_system_ping(self, data=bytes([0xde, 0xad, 0xbe, 0xef])):
        """ Ping flipper

        Parameters
        ----------
        data : bytes

        Raises
        ----------
        InputTypeException
        cmdException
        """
        cmd_data = system_pb2.PingRequest()

        if not isinstance(data, bytes):
            raise InputTypeException("Invalid Ping data value")

        cmd_data.data = data
        rep_data = self._cmd_send_and_read_answer(cmd_data, 'system_ping_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)

        return rep_data.system_ping_response.data

    # PlayAudiovisualAlert
    def cmd_system_audiovisual_alert(self):
        """
            Launch audiovisual alert on flipper ??
        """
        cmd_data = system_pb2.PlayAudiovisualAlertRequest()
        rep_data = self._cmd_send_and_read_answer(
            cmd_data, 'system_play_audiovisual_alert_request')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)


    def cmd_flipper_stop_session(self):
        """ Stop RPC session
        """
        cmd_data = flipper_pb2.StopSession()
        rep_data = self._cmd_send(
            cmd_data, 'stop_session')

        if rep_data.command_status != 0:
            raise cmdException(self.values_by_number[rep_data.command_status].name)
