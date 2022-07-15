# Python bindings for Flipper Zero protobuf protocol

Example:
```
#!/usr/bin/env python3

import os
import sys
import pprint
import datetime

from google.protobuf.json_format import MessageToDict
from flipperzero_protobuf.flipper_proto import FlipperProto
from flipperzero_protobuf.cli_helpers import *

def main():

    proto = FlipperProto()

    print("\n\nPing")
    ping_rep = proto.cmd_system_ping()
    print_hex(ping_rep)

    print("\n\n]DeviceInfo")
    ping_rep = proto.cmd_DeviceInfo()
    print(ping_rep)

    print("\n\nGetDateTime")
    dtime_resp = proto.cmd_GetDateTime()
    dt = dict2datetime(dtime_resp)
    print(dt.ctime())

    print("\n\nList files")
    list_resp = proto.cmd_storage_list('/ext')
    for li in list_resp:
        print(f"[{li['type']}]\t{li['name']}")



if __name__ == '__main__':
    main()
```
