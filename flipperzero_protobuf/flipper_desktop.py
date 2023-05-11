#!/usr/bin/env python3
"""
FlipperProtoDesktop system related function Class
"""

# import sys
# import os
import datetime

from google.protobuf.json_format import MessageToDict

from .flipper_base import FlipperProtoException, InputTypeException
from .flipperzero_protobuf_compiled import flipper_pb2, desktop_pb2

# import pprint

# from nis import match
# from numpy import mat

# pylint: disable=line-too-long, no-member


__all__ = ["FlipperProtoDesktop"]


class FlipperProtoDesktop:
    def desktop_is_locked(self) -> None:
        cmd_data = desktop_pb2.IsLockedRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, "desktop_is_locked_request")
        return rep_data.command_status

    def desktop_unlock(self) -> None:
        cmd_data = desktop_pb2.UnlockRequest()
        rep_data = self._rpc_send_and_read_answer(cmd_data, "desktop_unlock_request")
        return rep_data.command_status
