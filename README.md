# Python bindings for Flipper Zero protobuf protocol 


Python API binding/wrappers for Flipper Zero protobuf protocol and command line tool

---
### flipperzero_cmd ###

The command tool `flipperzero_cmd` is terminal based tool for file transfer and remote command.
It can be run from the command line or as an interactive app.

It is still a work in progress (Alpha) but is functional

---


### Command Line Examples ###

List and manage files from command line
```
$ flipperzero_cmd ls
Using port /dev/cu.usbmodemflip_Unyana1
.fseventsd/              .Spotlight-V100/         badusb/                  dolphin/
ibutton/                 infrared/                lfrfid/                  music_player/
nfc/                     subghz/                  u2f/                     wav_player/
.metadata_never_index    favorites.txt            Manifest                 rwfiletest.bin

```

Copy single files to fromFlipper device
```
$ flipperzero_cmd put My_Home_TV.ir /ext/infrared
Using port /dev/cu.usbmodemflip_UOhBaby
PUT My_Home_TV.ir /ext/infrared
putting 206 bytes

```

Copy directory tree to Flipper device
```
$ flipperzero_cmd put-tree subghz/samples /ext/subghz

```

#### Interactive Command Mode Examples ####


```
$ flipperzero_cmd
Using port /dev/cu.usbmodemflip_UOhBaby
Entering interactive mode

/ext flipper> help
    CAT                 : read flipper file to screen
    CD CHDIR            : change current directory on flipper
    DEV-INFO            : print device info
    DF INFO             : get Filesystem info
    DU DISK-USAGE       : display disk usage statistic
    GET GETFILE         : copy file from flipper
    GET-TREE GETTREE    : copy directory tree from flipper
    HELP ?              : print command list
    HISTORY HIST        : Print command history
    LCD LCHDIR          : Change local current directory
    LPWD                : print local working directory
    LS LIST             : list files and dirs on Flipper device
    MD MKDIR            : create a new directory
    MD5SUM MD5          : md5 hash of the file
    MV RENAME           : rename file or dir
    PRINT-SCREEN        : Take screendump in ascii or PBM format
    PUT PUTFILE         : copy file to flipper
    PUT-TREE PUTTREE    : copy directory tree to flipper
    QUIT EXIT           : Exit Program
    REBOOT              : reboot flipper
    RM DEL DELETE       : delete file of directory on flipper device
    SEND SEND-COMMAND   : Semd non rpc command to flipper
    SET                 : set or print current option value
    STAT                : get info about file or dir
    START-SESSION       : (re) start RPC session
    STOP-SESSION        : stop RPC session
    TIME                : Set or Get Current time from Flipper
    ZIP                 : Generate Zip Archive

```

```
/ext flipper> ls
.Spotlight-V100/         .Trashes/                apps/                    badusb/
dolphin/                 elf/                     ibutton/                 infrared/
lfrfid/                  music_player/            nfc/                     subghz/
u2f/                     wav_player/              .metadata_never_index    favorites.txt
Manifest                 rwfiletest.bin
```

```
/ext flipper> ls ?
Syntax :
	LS [-l] [-m] <path>
    
/ext flipper> ls -lm
Storage List result:  /ext
.Spotlight-V100          	   DIR
.Trashes                 	   DIR
apps                     	   DIR
badusb                   	   DIR
dolphin                  	   DIR
elf                      	   DIR
ibutton                  	   DIR
infrared                 	   DIR
lfrfid                   	   DIR
music_player             	   DIR
nfc                      	   DIR
subghz                   	   DIR
u2f                      	   DIR
wav_player               	   DIR
.metadata_never_index    	     0 d41d8cd98f00b204e9800998ecf8427e
favorites.txt            	    93 50c7a56f93d8f6c87f205691def774fa
Manifest                 	 16871 c74a84dea8d644198d27755313942614
rwfiletest.bin           	 16384 3df67097cee5e4cea36e0f941c134ffc
Total Bytes: 33348

/ext flipper> rcd infrared/
remote directory = /ext/infrared 

/ext/infrared flipper> ls
assets/                  IRDB/                    Sanyo/                   TV_Philips/
Minolta.ir               My_Home_TV.ir

/ext/infrared flipper> quit
Quit interactive mode
```


---

### API Examples: ###
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
    ping_rep = proto.rcp_system_ping()
    print_hex(ping_rep)

    print("\n\n]DeviceInfo")
    ping_rep = proto.rcp_device_info()
    print(ping_rep)

    print("\n\nGetDateTime")
    dtime_resp = proto.rcp_get_datetime()
    dt = dict2datetime(dtime_resp)
    print(dt.ctime())

    print("\n\nList files")
    list_resp = proto.rcp_storage_list('/ext')
    for li in list_resp:
        print(f"[{li['type']}]\t{li['name']}")



if __name__ == '__main__':
    main()
```

---

See Also:<br>
[flipperdevices/flipperzero-protobuf](http://github.com/flipperdevices/flipperzero-protobuf)<br>
[flipperdevices/go-flipper](https://github.com/flipperdevices/go-flipper)

