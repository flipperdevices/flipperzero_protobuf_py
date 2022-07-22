#!/usr/bin/env python3

import os
import sys
# import pprint


# /usr/local/Cellar/protobuf/3.19.4/lib/python3.10/site-packages/google/protobuf/json_format.py

from google.protobuf.json_format import MessageToDict
# from flipperzero_protobuf.flipper_protof import FlipperProto
from flipperzero_protobuf.flipper_base import FlipperProtoBase, cmdException
from flipperzero_protobuf.flipper_storage import FlipperProtoStorage

# pylint: disable=line-too-long, no-member
_debug = 0

DEV = "/dev/tty.usbmodemflip_Unyana1"

class QuitException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class FlipperCMD(FlipperProtoBase, FlipperProtoStorage):
    pass



commands_help = {
    "DF, INFO": "get FS info",

    "LS, LIST": "list files and dirs",
    "RM, DEL, DELETE" : "delete file or dir",
    "MD, MKDIR" : "creates a new directory",
    "MV, RENAME" : "rename file or dir",

    "STAT" : "get info about file or dir",

    "CD, CHDIR" : "change local working directory",
    "PWD": "print local working directory",

    "MD5, MD5SUM" : "md5 hash of the file",
    "PUT, PUTFILE": "copy file to flipper",
    "GET, GETFILE": "copy file from flipper",
    "CAT": "read file to screen",

    "HELP, ?" : "print command list",
    # "VERBOSE" : "set verbose",
    # "ERROR" : "print last error",
    "EXIT, QUIT" : "exit program",
}


rdir = '/ext'

def main():

    global rdir
    interactive = False

    proto = FlipperCMD()

    argv = sys.argv[1:]

    if len(argv) == 0:
        print("Entering interactive mode")
        import shlex
        interactive = True

    lineno = 1
    while 1:
        try:

            if interactive is True:
                print(f"{lineno} flipper> ", end="")
                argv = shlex.split(input(), comments=True, posix=True)
                if argv is None or len(argv) == 0:
                    continue

            lineno += 1
            run_comm(proto, argv)

        except (EOFError, QuitException) as _e:
            interactive = False
            break
        except cmdException as e:
            print(e)
        finally:
            if interactive is not True:
                return


def run_comm(flip, argv):
    global verbose

    cmd = argv.pop(0).upper()

    if cmd in ["LS", "LIST" ]:
        do_list(flip, cmd, argv)

    elif cmd in ["RM", "DEL", "DELETE"]:
        do_del(flip, cmd, argv)

    elif cmd in ["MV", "RENAME"]:
        do_rename(flip, cmd, argv)

    elif cmd in ["MD", "MKDIR"]:
        do_mkdir(flip, cmd, argv)

    elif cmd in ["MD5SUM", "MD5"]:
        do_md5sum(flip, cmd, argv)

    elif cmd in ["CAT"]:
        do_cat_file(flip, cmd, argv)

    elif cmd in ["GET", "GETFILE"]:
        do_get_file(flip, cmd, argv)

    elif cmd in ["PUT", "PUTFILE"]:
        do_put_file(flip, cmd, argv)

    elif cmd in ["STAT"]:
        do_stat(flip, cmd, argv)

    elif cmd in ["DF", "INFO"]:
        do_info(flip, cmd, argv)

    elif cmd in ["CD", "CHDIR", "!CD", "!CHDIR"]:
        do_chdir(flip, cmd, argv)

    elif cmd in ["PWD"]:
        print(os.getcwd())

    elif cmd in ["RCD"]:
        set_rdir(flip, cmd, argv)

    elif cmd in ["QUIT", "EXIT"]:
        raise QuitException("Quit interactive mode")

    elif cmd in ["HELP", "?"]:
        print_cmds()

    else:
        print("Unknown command : ", cmd)  # str(" ").join(argv)


def print_cmds(cmd_list=None):
    if cmd_list is None:
        cmd_list = commands_help
    for k, v in cmd_list.items():
        print(f"    {k:<22} :\t{v}")
    # print "\nFor more detail on command run command with arg '?'"
    # print "\n* == may not be implemented\n"

def set_rdir(flip, remdir):
    global rdir

    if remdir.startswith('/'):
        newdir = remdir
    else:
        newdir = os.path.abspath(rdir + '/' + remdir)

    stat_resp = flip.cmd_stat(newdir)
    if stat_resp['type'] == 'DIR':
        rdir = newdir
    else:
        print("{newdir}: not a directory")

# storage_pb2.File.DIR == 1
# storage_pb2.File.FILE == 0
def do_list(flip, cmd, argv):

    targ = '/ext'
    long_format = False
    md5_format = False

    while len(argv) > 0 and argv[0][0]== "-":
        if argv[0] == "-l":
            long_format = True
            argv.pop(0)
        elif argv[0] in [ '-m', '-ml', '-lm' ]:
            long_format = True
            md5_format = True
            argv.pop(0)
        elif argv[0] in ['help', '?']:
            raise cmdException(f"Syntax :\n\t{cmd} [-l] [-m] <path>")

    #if len(argv) > 0 and argv[0] == "-l":
    #    long_format = True
    #    argv.pop(0)

    if len(argv) > 0:
        targ = argv.pop(0)

    print(f"do_list {targ}")
    print(f"long_format={long_format}, md5_format={md5_format}")

    if not targ.startswith('/'):
        targ = '/ext/' + targ

    if len(targ) > 1:
        targ = targ.rstrip('/')

    flist = flip.cmd_storage_list(targ)
    flist.sort(key = lambda x: (x['type'], x['name'].lower() ))

    if _debug:
        print("Storage List result: ", targ)

    if long_format:
        # dir_fmt = "{:<25s}\t   DIR"
        # file_fmt = "{:<25s}\t{:>6d}\t{}"
        md5val = ""
        sizetotal = 0

        print(f"{targ}:")
        for l in flist:
            if l['type'] == 'DIR':
                # print(dir_fmt.format(l['name'])
                print(f"{l['name']:<25s}\t   DIR")
            else:
                sizetotal += l['size']
                if md5_format:
                    md5val = flip.cmd_md5sum(targ + '/' + l['name'])
                    print(f"{l['name']:<25s}\t{l['size']:>6d}", md5val)
                else:
                    print(f"{l['name']:<25s}\t{l['size']:>6d}")
        print(f"Total Bytes: {sizetotal}")
    else:
        j = 1
        for l in flist:
            j += 1
            endl = ""

            if l['type'] == 'DIR':
                name = l['name'] + '/'
            else:
                name = l['name']

            if j % 4  == 1:
                endl = '\n'

            print(f"{name:<25s}", end=endl)

    print()
    # pprint.pprint(flist)



def do_del(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} file")

    targ = argv.pop(0)

    del_resp = flip.cmd_delete(targ)

    if _debug:
        print(f"del_resp={del_resp}")


def do_rename(flip, cmd, argv):
    """
        rename file glue
    """
    if ( len(argv) > 1  and argv[0] != "?" ):
        old_fn = argv.pop(0)
        new_fn = argv.pop(0)

        if not old_fn.startswith('/'):
            old_fn = '/ext/' + old_fn

        if not new_fn.startswith('/'):
            new_fn = '/ext/' + new_fn

        if _debug:
            print(cmd, old_fn, new_fn)

        rename_resp = flip.cmd_rename_file(old_fn, new_fn)

        if _debug:
            print(f"rename_resp={rename_resp}")

    else:
        raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")


def do_mkdir(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} file")

    targ = argv.pop(0)
    if not targ.startswith('/'):
        targ = '/ext/' + targ

    if _debug:
        print(cmd, targ)

    flip.cmd_mkdir(targ)


def do_chdir(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} <directory>")

    targ = argv.pop(0)

    try:
        os.chdir(targ)
    except FileNotFoundError as _e:
        print(f"No such file or directory: {targ}")
    except NotADirectoryError as _e:
        print(f"Not a directory: {targ}")
    except Exception as _e:
        print(f"CHDIR: {_e}")


def do_md5sum(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} file")

    targ = argv.pop(0)

    if not targ.startswith('/'):
        targ = '/ext/' + targ

    if _debug:
        print(cmd, targ)

    md5sum_resp = flip.cmd_md5sum(targ)
    print(f"md5sum_resp={md5sum_resp}")


def do_cat_file(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} file")

    remote_filen = argv.pop(0)

    if not remote_filen.startswith('/'):
        remote_filen = '/ext/' + remote_filen

    if _debug:
        print(cmd, remote_filen)

    read_resp = flip.cmd_read(remote_filen)
    # print("cmd_read {len(read_resp)}")
    print(read_resp)


def do_get_file(flip, cmd, argv):
    if ( len(argv) >= 1 and argv[0] != "?" ):
        remote_filen = argv.pop(0)
        if argv:
            local_filen = argv.pop(0)
        else:
            local_filen = "."

        if os.path.isdir(local_filen):
            local_filen = local_filen + "/" + os.path.basename(remote_filen)

        if not remote_filen.startswith('/'):
            remote_filen = '/ext/' + remote_filen

        if _debug:
            print( cmd, remote_filen, local_filen)

        read_resp = flip.cmd_read(remote_filen)
        print(f"getting {len(read_resp)} bytes")
        with open(local_filen, 'wb') as fd:
            fd.write(read_resp)
    else:
        raise cmdException(f"Syntax :\n\t{cmd} <remote_filename> <local_filename>")


def do_put_file(flip, cmd, argv):
    if ( len(argv) >= 1  and argv[0] != "?" ):
        local_filen = argv.pop(0)
        if argv:
            remote_Filen = argv.pop(0)
        else:
            remote_Filen = local_filen

        if _debug:
            print( cmd, remote_Filen, local_filen)

        if not os.path.exists(local_filen):
            print(f"can not open {local_filen}")
        elif os.path.isdir(local_filen):
            print(f"Is a directory  {local_filen}")
            return

        if not remote_filen.startswith('/'):
            remote_filen = '/ext/' + remote_filen

        stat_resp = flip.cmd_stat(remote_filen)
        if stat_resp['type'] == 'DIR':
            remote_filen = remote_filen + '/' + local_filen

        with open(local_filen, 'rb') as fd:
            file_data = fd.read()

        print(f"putting {len(file_data)} bytes")
        flip.cmd_write(remote_Filen, file_data)

    else:
        raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")


def do_info(flip, cmd, argv):
    targ = '/ext'

    if len(argv) > 0:
        targ = argv.pop(0)

    if not targ.startswith('/'):
        targ = '/ext/' + targ

    if _debug:
        print(cmd, targ)

    info_resp = flip.cmd_info('/ext/')

    tspace = int(info_resp['totalSpace'])
    fspace = int(info_resp['freeSpace'])
    print(f"filesystem: {targ}\n"
          f"totalSpace: {tspace}\nfreeSpace:  {fspace}\n"
          f"usedspace:  {tspace - fspace}\n")

def do_stat(flip, cmd, argv):
    if ( len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
        raise cmdException(f"Syntax :\n\t{cmd} file")

    targ = argv.pop(0)

    if not targ.startswith('/'):
        targ = '/ext/' + targ

    targ = targ.rstrip('/')

    if _debug:
        print(cmd, targ)

    stat_resp = flip.cmd_stat(targ)

    if _debug:
        print(f"stat_resp={stat_resp}")


    #if stat_resp.get('commandId', 0) != 0:
    #    print(f"Error: {stat_resp['commandStatus']}")
    #    return


    if stat_resp['type'] == 'DIR':
        print(f"{targ:<25s}\t   DIR")
    else:
        print(f"{targ:<25s}\t{stat_resp['size']:>6d}")


if __name__ == '__main__':
    main()
