# Python bindings for Flipper Zero protobuf protocol 


Python API binding/wrappers for Flipper Zero protobuf protocol and command line tool

---
### flipperzero_cmd 

The command tool `flipperzero_cmd` is terninal based too for file transfer and remote command.
It can be run from the command line or as an interactive app.

It is still a work in progress (Alpha) but is funtional

---

##### Command Line #####

```
$ flipperzero_cmd ls
Using port /dev/cu.usbmodemflip_Unyana1
.fseventsd/              .Spotlight-V100/         badusb/                  dolphin/
ibutton/                 infrared/                lfrfid/                  music_player/
nfc/                     subghz/                  u2f/                     wav_player/
.metadata_never_index    favorites.txt            Manifest                 rwfiletest.bin
```

##### interactive command moode #####


```
$ ./test_cmd.py
Using port /dev/cu.usbmodemflip_UOhBaby
Entering interactive mode

1 flipper> help
    DF, INFO               :	get FS info
    LS, LIST               :	list files and dirs
    RM, DEL, DELETE        :	delete file or dir
    MD, MKDIR              :	creates a new directory
    MV, RENAME             :	rename file or dir
    STAT                   :	get info about file or dir
    CD, CHDIR              :	change local working directory
    PWD                    :	print local working directory
    MD5, MD5SUM            :	md5 hash of the file
    PUT, PUTFILE           :	copy file to flipper
    GET, GETFILE           :	copy file from flipper
    CAT                    :	read file to screen
    PRINT-SCREEN           :	print ascii screendump
    HELP, ?                :	print command list
    EXIT, QUIT             :	exit program

2 flipper> ls
.fseventsd/              .Spotlight-V100/         badusb/                  dolphin/
ibutton/                 infrared/                lfrfid/                  music_player/
nfc/                     subghz/                  u2f/                     wav_player/
.metadata_never_index    favorites.txt            Manifest                 rwfiletest.bin

3 flipper> quit
Quit interactive mode
```
---

#### API example: ####
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
