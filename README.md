# Python bindings for Flipper Zero protobuf protocol 


Python API binding/wrappers for Flipper Zero protobuf protocol and command line tool

---
### flipperzero_cmd 

The command tool `flipperzero_cmd` is terminal based tool for file transfer and remote command.
It can be run from the command line or as an interactive app.

It is still a work in progress (Alpha) but is functional

---

##### Command Line Examples #####

```
$ flipperzero_cmd ls
Using port /dev/cu.usbmodemflip_Unyana1
.fseventsd/              .Spotlight-V100/         badusb/                  dolphin/
ibutton/                 infrared/                lfrfid/                  music_player/
nfc/                     subghz/                  u2f/                     wav_player/
.metadata_never_index    favorites.txt            Manifest                 rwfiletest.bin

```

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

##### Interactive Command Mode Examples #####


```
$ flipperzero_cmd
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
    PUT-TREE               :	copy directory tree to flipper
    GET, GETFILE           :	copy file from flipper
    GET-TREE               :	copy directory tree from flipper

    CAT                    :	read file to screen

    PRINT-SCREEN           :	screendump in ascii or PBM format

    RCD, RCHDIR            :	change current directory on flipper

    HISTORY                :	print command History
    HELP, ?                :	print command list
    DEBUG                  :	set or print current debug value
    EXIT, QUIT             :	exit program

2 flipper> ls ?
Syntax :
	LS [-l] [-m] <path>
    
3 flipper> ls -lm
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

3 flipper> quit
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
