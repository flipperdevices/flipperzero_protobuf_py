#!/usr/bin/env python3

# import sys
# import os
import datetime
import pprint

# from nis import match
# from numpy import mat

# pylint: disable=line-too-long, no-member

from google.protobuf.json_format import MessageToDict
from .flipperzero_protobuf_compiled import system_pb2, flipper_pb2
from .flipper_base import cmdException

__all__ = [ 'FlipperProtoSys']


class FlipperProtoSys:

    # FactoryReset

    # Update
    def cmd_Update(self, update_manifest=""):
        """Update"""
        cmd_data = system_pb2.UpdateRequest()
        cmd_data.update_manifest = update_manifest
        #print(MessageToDict(message=cmd_data, including_default_value_fields=True))
        #print(cmd_data.DESCRIPTOR.enum_types_by_name.keys())  # ['CommandStatus'].values_by_number
        #print(dir(cmd_data.update_manifest))
        data = self._cmd_send_and_read_answer(cmd_data, 'system_update_request')
        #print( MessageToDict(message=data.system_power_info_response))
        if data.command_status != 0:
            raise cmdException(self.values_by_number[data.command_status].name)
        return data.system_update_response

    # Reboot
    def cmd_Repoot(self, mode=0):
        """Reboot flipper"""
        # mode
        # 0 = OS
        # 1 = DFU
        # 2 = UPDATE
        cmd_data = system_pb2.RebootRequest()

        print(dir(cmd_data))
        cmd_data.mode = mode
        # print(MessageToDict(message=cmd_data, including_default_value_fields=True))
        #data = self._cmd_send(cmd_data, 'system_reboot_request')
        try:
            data = self._cmd_send_and_read_answer(cmd_data, 'system_reboot_request')
            #return data.system_reboot_response
        # except serial.serialutil.SerialException as _e:
        except Exception as _e:
            pass

    # PowerInfo
    def cmd_PowerInfo(self):
        """Power Info"""
        cmd_data = system_pb2.PowerInfoRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'system_power_info_request')
        return data.system_power_info_response
        # return MessageToDict(message=data.system_power_info_response)

    # DeviceInfo
    def cmd_DeviceInfo(self):
        """Power Info"""
        cmd_data = system_pb2.DeviceInfoRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'system_device_info_request')
        # return data.system_device_info_response
        return MessageToDict(message=data.system_device_info_response)

    # ProtobufVersion
    def cmd_ProtobufVersion(self):
        """ProtobufVersion"""
        cmd_data = system_pb2.ProtobufVersionRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'system_protobuf_version_request')
        if data.command_status != 0:
            raise cmdException(self.values_by_number[data.command_status].name)
        return data.system_protobuf_version_response

    # GetDateTime
    def cmd_GetDateTime(self):
        """Get Date Time"""
        cmd_data = system_pb2.GetDateTimeRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'system_get_datetime_request')
        if data.command_status != 0:
            raise cmdException(self.values_by_number[data.command_status].name)
        return MessageToDict(data.system_get_datetime_response)['datetime']

    # SetDateTime
    def cmd_SetDateTime(self, datetm=None):
        """Set Date Time"""
        if datetm is None:
            datetm = datetime.datetime.now()
        cmd_data = system_pb2.SetDateTimeRequest()
        print("SetDateTimeRequest", dir(cmd_data))
        print("SetDateTimeRequest.datetime", dir(cmd_data.datetime))
        cmd_data.datetime.year = datetm.year
        cmd_data.datetime.month = datetm.month
        cmd_data.datetime.day = datetm.day
        cmd_data.datetime.hour = datetm.hour
        cmd_data.datetime.minute = datetm.minute
        cmd_data.datetime.second = datetm.second
        cmd_data.datetime.weekday = datetm.isoweekday()
        print(datetm.timetuple())
        print(MessageToDict(message=cmd_data))

        data = self._cmd_send_and_read_answer(cmd_data, 'system_set_datetime_request')
        print("SetDateTimeRequest data", dir(data))
        print("SetDateTimeRequest data", MessageToDict(message=data))

        if data.command_status != 0:
            raise cmdException(self.values_by_number[data.command_status].name)
        return

    # Ping
    def cmd_system_ping(self, data=bytes([0xde, 0xad, 0xbe, 0xef])):
        """Ping flipper"""
        cmd_data = system_pb2.PingRequest()
        cmd_data.data = data
        data = self._cmd_send_and_read_answer(cmd_data, 'system_ping_request')
        return data.system_ping_response.data

    # PlayAudiovisualAlert
    def cmd_system_audiovisual_alert(self):
        """Launch audiovisual alert on flipper"""
        cmd_data = system_pb2.PlayAudiovisualAlertRequest()
        data = self._cmd_send_and_read_answer(
            cmd_data, 'system_play_audiovisual_alert_request')
        return data

    def cmd_flipper_stop_session(self):
        """Stop RPC session"""
        cmd_data = flipper_pb2.StopSession()
        data = self._cmd_send(
            cmd_data, 'stop_session')
        return data
