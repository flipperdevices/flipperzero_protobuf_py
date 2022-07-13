#!/usr/bin/env python3

# pylint: disable=line-too-long, no-member

from .flipperzero_protobuf_compiled import application_pb2

__all__ = [ 'FlipperProtoApp']

class FlipperProtoApp:

    # LockStatus
    def cmd_LockStatus(self):
        """Send exit command to app"""
        cmd_data = application_pb2.LockStatusRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'app_lock_status_request')

        if data.command_status != 0:
             raise cmdException(self.values_by_number[rep_data.command_status].name)

        return data.app_lock_status_response.locked

    # Start
    def cmd_app_start(self, name, args):
        """Start application"""
        cmd_data = application_pb2.StartRequest()
        cmd_data.name = name
        cmd_data.args = args
        data = self._cmd_send_and_read_answer(cmd_data, 'app_start_request')
        return data

    # AppExit
    def cmd_app_exit(self):
        """Send exit command to app"""
        cmd_data = application_pb2.AppExitRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'app_exit_request')
        return data

    # AppLoadFile
    def cmd_app_load_file(self, path):
        """Send load file command to app"""
        cmd_data = application_pb2.AppLoadFileRequest()
        cmd_data.path = path
        data = self._cmd_send_and_read_answer(cmd_data, 'app_load_file_request')
        return data

    # AppButtonPress
    def cmd_app_button_press(self, args):
        """Send button press command to app"""
        cmd_data = application_pb2.AppButtonPressRequest()
        cmd_data.args = args
        data = self._cmd_send_and_read_answer(cmd_data, 'app_button_press_request')
        return data

    # AppButtonRelease
    def cmd_app_button_release(self):
        """Send button release command to app"""
        cmd_data = application_pb2.AppButtonReleaseRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'app_button_release_request')
        return data
