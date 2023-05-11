#!/usr/bin/env python3
"""Meta command class for FlipperProto"""

# pylint: disable=too-few-public-methods


from .flipper_app import FlipperProtoApp
from .flipper_base import FlipperProtoBase
from .flipper_gpio import FlipperProtoGpio
from .flipper_desktop import FlipperProtoDesktop
from .flipper_gui import FlipperProtoGui
from .flipper_property import FlipperProtoProperty
from .flipper_storage import FlipperProtoStorage
from .flipper_sys import FlipperProtoSys

# from .flipperzero_protobuf_compiled import flipper_pb2, system_pb2, gui_pb2, gpio_pb2

__all__ = ["FlipperProto"]


class FlipperProto(
    FlipperProtoBase,
    FlipperProtoDesktop,
    FlipperProtoSys,
    FlipperProtoGpio,
    FlipperProtoApp,
    FlipperProtoGui,
    FlipperProtoStorage,
    FlipperProtoProperty,
):
    """
    Meta command class
    """

    # pylint: disable=unnecessary-pass
    pass
