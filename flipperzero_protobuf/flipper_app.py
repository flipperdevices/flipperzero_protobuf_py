#!/usr/bin/env python3

# pylint: disable=line-too-long, no-member

from .flipperzero_protobuf_compiled import application_pb2
from .flipper_base import cmdException

__all__ = ['FlipperProtoApp']


class FlipperProtoApp:

    # LockStatus
    def rpc_lock_status(self) -> bool:
        """ Get LockScreen Status

        Returns
        ----------
        bool

        Raises
        ----------
        cmdException

        """
        cmd_data = application_pb2.LockStatusRequest()
        data = self._rpc_send_and_read_answer(cmd_data, 'app_lock_status_request')

        if data.command_status != 0:
            raise cmdException(self.Status_values_by_number[data.command_status].name)

        return data.app_lock_status_response.locked

    # Start
    def rpc_app_start(self, name, args) -> None:
        """ Start/Run application

        Parameters
        ----------
        name : str
        args : str

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """
        cmd_data = application_pb2.StartRequest()
        cmd_data.name = name
        cmd_data.args = args
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'app_start_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # AppExit
    def rpc_app_exit(self) -> None:
        """Send exit command to app

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """
        cmd_data = application_pb2.AppExitRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'app_exit_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # AppLoadFile
    def rpc_app_load_file(self, path) -> None:
        """Send load file command to app.

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """

        cmd_data = application_pb2.AppLoadFileRequest()
        cmd_data.path = path
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'app_load_file_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # AppButtonPress
    def rpc_app_button_press(self, args) -> None:
        """Send button press command to app.

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """

        cmd_data = application_pb2.AppButtonPressRequest()
        cmd_data.args = args
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'app_button_press_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)

    # AppButtonRelease
    def rpc_app_button_release(self) -> None:
        """Send button release command to app

        Returns
        ----------
        None

        Raises
        ----------
        cmdException

        """
        cmd_data = application_pb2.AppButtonReleaseRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, 'app_button_release_request')
        if rep_data.command_status != 0:
            raise cmdException(self.Status_values_by_number[rep_data.command_status].name)
