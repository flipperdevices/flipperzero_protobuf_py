#!/usr/bin/env python3
"""
FlipperProto property related function Class
"""

# import sys
# import os
import datetime

from google.protobuf.json_format import MessageToDict

from .flipper_base import FlipperProtoException, InputTypeException
from .flipperzero_protobuf_compiled import flipper_pb2, property_pb2

# import pprint

# from nis import match
# from numpy import mat

# pylint: disable=line-too-long, no-member


__all__ = ["FlipperProtoProperty"]


class FlipperProtoProperty:
    """FlipperProto property function Class"""

    # CommonInfo
    def rpc_property_get(self, key: str) -> list[tuple[str, str]]:
        """Property get

        Return
        ----------
        list[tuple[key, value : str]]

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = property_pb2.GetRequest()
        cmd_data.key = key

        rep_data = self._rpc_send_and_read_answer(cmd_data, "property_get_request")

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                self.Status_values_by_number[rep_data.command_status].name
            )

        ret = []

        while rep_data.has_next:
            ret.append(
                (
                    rep_data.property_get_response.key,
                    rep_data.property_get_response.value,
                )
            )

            rep_data = self._rpc_read_answer()

        return ret
