#!/usr/bin/env python3
# pylint: disable=line-too-long, no-member, too-many-branches, unused-import

import os
import sys
import readline
import shlex
# import pprint


# from google.protobuf.json_format import MessageToDict
from .flipper_base import cmdException    # FlipperProtoBase
# from .flipper_storage import FlipperProtoStorage
from .flipper_proto import FlipperProto
from .cli_helpers import print_screen

_DEBUG = 0

# class FlipperCMD(FlipperProtoBase, FlipperProtoStorage):
#    pass


COMMANDS_HELP = {
    "DF, INFO": "get FS info",

    "LS, LIST": "list files and dirs",
    "RM, DEL, DELETE": "delete file or dir",
    "MD, MKDIR": "creates a new directory",
    "MV, RENAME": "rename file or dir",

    "STAT": "get info about file or dir",

    "CD, CHDIR": "change local working directory",
    "PWD": "print local working directory",

    "MD5, MD5SUM": "md5 hash of the file",
    "PUT, PUTFILE": "copy file to flipper",
    "GET, GETFILE": "copy file from flipper",
    "CAT": "read file to screen",

    "PRINT-SCREEN": "print ascii screendump",

    "RCD": "change current directory on flipper",

    "HELP, ?": "print command list",
    # "VERBOSE": "set verbose",
    "DEBUG": "set or print current debug value",

    # "ERROR": "print last error",
    "EXIT, QUIT": "exit program",
}


class FlipperCMD:

    class QuitException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)

    commands_help = COMMANDS_HELP

    def __init__(self, proto=None, debug=_DEBUG):

        if proto is None:
            self.flip = FlipperProto()

        self.rdir = '/ext'

        self.debug = debug

    def run_comm(self, argv):
        # global verbose

        cmd = argv.pop(0).upper()

        if cmd in ["LS", "LIST"]:
            self.do_list(cmd, argv)

        elif cmd in ["RM", "DEL", "DELETE"]:
            self.do_del(cmd, argv)

        elif cmd in ["MV", "RENAME"]:
            self.do_rename(cmd, argv)

        elif cmd in ["MD", "MKDIR"]:
            self.do_mkdir(cmd, argv)

        elif cmd in ["MD5SUM", "MD5"]:
            self.do_md5sum(cmd, argv)

        elif cmd in ["CAT"]:
            self.do_cat_file(cmd, argv)

        elif cmd in ["GET", "GETFILE"]:
            self.do_get_file(cmd, argv)

        elif cmd in ["PUT", "PUTFILE"]:
            self.do_put_file(cmd, argv)

        elif cmd in ["STAT"]:
            self.do_stat(cmd, argv)

        elif cmd in ["DF", "INFO"]:
            self.do_info(cmd, argv)

        elif cmd in ["CD", "CHDIR", "!CD", "!CHDIR"]:
            self.do_chdir(cmd, argv)

        elif cmd in ["PWD"]:
            print(os.getcwd())

        elif cmd in ["PRINT-SCREEN"]:
            self.do_print_screen(cmd, argv)

        elif cmd in ["RCD"]:
            self.set_rdir(cmd, argv)

        elif cmd in ["DEBUG"]:
            self.set_debug(cmd, argv)

        elif cmd in ["QUIT", "EXIT"]:
            raise self.QuitException("Quit interactive mode")

        elif cmd in ["HELP", "?"]:
            self.print_cmd_help()

        else:
            print("Unknown command : ", cmd)  # str(" ").join(argv)

    def print_cmd_help(self, cmd_list=None):
        if cmd_list is None:
            cmd_list = COMMANDS_HELP
        for k, v in cmd_list.items():
            print(f"    {k:<22} :\t{v}")
        # print "\nFor more detail on command run command with arg '?'"
        # print "\n* == may not be implemented\n"

    def set_debug(self, cmd, argv):
        if len(argv) < 1:
            print(f"DEBUG = {self.debug}")
            return

        opt = argv.pop(0).upper()

        if opt in ["ON", "TRUE"]:
            self.debug = 1
        elif opt in ["++"]:
            self.debug += 1
        elif opt in ["--"]:
            self.debug -= 1
            debug = max(debug, 0)
        elif opt.isdigit():
            self.debug = int(opt)
        elif opt in ["?", "HELP"]:
            print(f"{cmd}: [DEBUG_LEVEL]\n"
                  "\tshows current level if no arg is given")

        else:
            print(f"{cmd}: unknown option: {opt}")

    # pylint: disable=protected-access
    def set_rdir(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} <DIR>\n"
                               "\tset remote directory")

        remdir = argv.pop(0)

        if remdir.startswith('/'):
            newdir = remdir
        else:
            newdir = os.path.abspath(self.rdir + '/' + remdir)

        if newdir in ['/', '/ext', '/int']:
            self.rdir = newdir
            print(f"Remote directory: {newdir}")

        stat_resp = self.flip._cmd_stat(newdir)

        # if self.debug:
        #     print(f"{cmd}:\n\tremdir={remdir}\n\tnewdir={newdir}\ni\tstat_resp={stat_resp}")

        if stat_resp is None:
            print("f{newdir}: Not found")
        elif stat_resp['type'] == 'DIR':
            self.rdir = newdir
        else:
            print("{newdir}: not a directory")

        print(f"Remote directory: {newdir}")

    def do_print_screen(self, cmd, argv):
        outf = None
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} [filename.pbm]\n"
                               "\tfile has to end in .pbm\n"
                               "\tif no file is given image is printed to stdout")

        if argv:
            outf = argv.pop(0)
        print_screen(self.flip.cmd_gui_snapshot_screen(), outf)

    # storage_pb2.File.DIR == 1
    # storage_pb2.File.FILE == 0

    def do_list(self, cmd, argv):
        # pylint: disable=protected-access

        targ = self.rdir
        long_format = False
        md5_format = False

        while len(argv) > 0 and argv[0][0] in ["-", "?"]:
            # print(f"do_list argv0 {argv}")
            if argv[0] == "-l":
                long_format = True
                argv.pop(0)
            elif argv[0] in ['-m', '-ml', '-lm']:
                long_format = True
                md5_format = True
                argv.pop(0)
            elif argv[0] in ['-help', '?']:
                raise cmdException(f"Syntax :\n\t{cmd} [-l] [-m] <path>")

        # if len(argv) > 0 and argv[0] == "-l":
        #    long_format = True
        #    argv.pop(0)

        if len(argv) > 0:
            targ = argv.pop(0)

        # if self.debug:
        #     print(f"{cmd} = targ={targ}")

        # print(f"do_list {targ}")
        # print(f"long_format={long_format}, md5_format={md5_format}")

        if not targ.startswith('/'):
            # targ = '/ext/' + targ
            targ = os.path.abspath(self.rdir + '/' + targ)

        if len(targ) > 1:
            targ = targ.rstrip('/')

        flist = self.flip.cmd_storage_list(targ)
        flist.sort(key=lambda x: (x['type'], x['name'].lower()))

        if self.debug:
            print("Storage List result: ", targ)

        if long_format:
            # dir_fmt = "{:<25s}\t   DIR"
            # file_fmt = "{:<25s}\t{:>6d}\t{}"
            md5val = ""
            sizetotal = 0

            print(f"{targ}:")
            for line in flist:
                if line['type'] == 'DIR':
                    # print(dir_fmt.format(line['name'])
                    print(f"{line['name']:<25s}\t   DIR")
                else:
                    sizetotal += line['size']
                    if md5_format:
                        md5val = self.flip.cmd_md5sum(targ + '/' + line['name'])
                        print(f"{line['name']:<25s}\t{line['size']:>6d}", md5val)
                    else:
                        print(f"{line['name']:<25s}\t{line['size']:>6d}")
            print(f"Total Bytes: {sizetotal}")
        else:
            j = 1
            for line in flist:
                j += 1
                endl = ""

                if line['type'] == 'DIR':
                    name = line['name'] + '/'
                else:
                    name = line['name']

                if j % 4 == 1:
                    endl = '\n'

                print(f"{name:<25s}", end=endl)

        # add blank line
        print()
        # pprint.pprint(flist)

    def do_del(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)
        if not targ.startswith('/'):
            targ = os.path.abspath(self.rdir + '/' + targ)

        del_resp = self.flip.cmd_delete(targ)

        if self.debug:
            print(f"del_resp={del_resp}")

    def do_rename(self, cmd, argv):
        """
            rename file glue
        """
        if (len(argv) > 1 and argv[0] != "?"):
            old_fn = argv.pop(0)
            new_fn = argv.pop(0)

            if not old_fn.startswith('/'):
                old_fn = os.path.abspath(self.rdir + '/' + old_fn)

            if not new_fn.startswith('/'):
                new_fn = os.path.abspath(self.rdir + '/' + new_fn)

            if self.debug:
                print(cmd, old_fn, new_fn)

            rename_resp = self.flip.cmd_rename_file(old_fn, new_fn)

            if self.debug:
                print(f"rename_resp={rename_resp}")

        else:
            raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")

    def do_mkdir(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)
        if not targ.startswith('/'):
            targ = os.path.abspath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        self.flip.cmd_mkdir(targ)

    def do_chdir(self, cmd, argv):
        # pylint: disable=broad-except, unused-argument
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
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

    def do_md5sum(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.abspath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        md5sum_resp = self.flip.cmd_md5sum(targ)
        print(f"md5sum_resp={md5sum_resp}")

    def do_cat_file(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        remote_filen = argv.pop(0)

        if not remote_filen.startswith('/'):
            remote_filen = os.path.abspath(self.rdir + '/' + remote_filen)

        if self.debug:
            print(cmd, remote_filen)

        read_resp = self.flip.cmd_read(remote_filen)
        # print("cmd_read {len(read_resp)}")
        print(read_resp)

    def do_get_file(self, cmd, argv):
        if (len(argv) >= 1 and argv[0] != "?"):
            remote_filen = argv.pop(0)
            if argv:
                local_filen = argv.pop(0)
            else:
                local_filen = "."

            if os.path.isdir(local_filen):
                local_filen = local_filen + "/" + os.path.basename(remote_filen)

            if not remote_filen.startswith('/'):
                remote_filen = os.path.abspath(self.rdir + '/' + remote_filen)

            if self.debug:
                print(cmd, remote_filen, local_filen)

            read_resp = self.flip.cmd_read(remote_filen)
            print(f"getting {len(read_resp)} bytes")
            with open(local_filen, 'wb') as fd:
                fd.write(read_resp)
        else:
            raise cmdException(f"Syntax :\n\t{cmd} <remote_filename> <local_filename>")

    def do_put_file(self, cmd, argv):
        if (len(argv) >= 1 and argv[0] != "?"):
            local_filen = argv.pop(0)
            if argv:
                remote_filen = argv.pop(0)
            else:
                remote_filen = local_filen

            if self.debug:
                print(cmd, local_filen, remote_filen)

            if not os.path.exists(local_filen):
                print(f"can not open {local_filen}")
            elif os.path.isdir(local_filen):
                print(f"Is a directory  {local_filen}")
                return

            if not remote_filen.startswith('/'):
                remote_filen = os.path.abspath(self.rdir + '/' + remote_filen)

            stat_resp = self.flip._cmd_stat(remote_filen)
            # print("stat_resp=",stat_resp)
            if stat_resp is not None and stat_resp.get('type', "") == 'DIR':
                remote_filen = remote_filen + '/' + local_filen

            # print(cmd, local_filen, remote_filen)

            with open(local_filen, 'rb') as fd:
                file_data = fd.read()

            print(f"putting {len(file_data)} bytes")
            self.flip.cmd_write(remote_filen, file_data)

        else:
            raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")

    def do_info(self, _cmd, argv):
        targ = '/ext'

        if len(argv) > 0:
            targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.abspath(self.rdir + '/' + targ)

        # if self.debug:

        # print(cmd, targ)

        info_resp = self.flip.cmd_info(targ)

        tspace = int(info_resp['totalSpace'])
        fspace = int(info_resp['freeSpace'])
        print(f"filesystem: {targ}\n"
              f"totalSpace: {tspace}\nfreeSpace:  {fspace}\n"
              f"usedspace:  {tspace - fspace}\n")

    def do_stat(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.abspath(self.rdir + '/' + targ)

        targ = targ.rstrip('/')

        if self.debug:
            print(cmd, targ)

        stat_resp = self.flip.cmd_stat(targ)

        if self.debug:
            print(f"stat_resp={stat_resp}")

        # if stat_resp.get('commandId', 0) != 0:
        #    print(f"Error: {stat_resp['commandStatus']}")
        #    return

        if stat_resp['type'] == 'DIR':
            print(f"{targ:<25s}\t   DIR")
        else:
            print(f"{targ:<25s}\t{stat_resp['size']:>6d}")


def main():

    # global rdir
    interactive = False

    fcmd = FlipperCMD()
    # proto = FlipperProto()

    argv = sys.argv[1:]

    if len(argv) == 0:
        print("Entering interactive mode")
        interactive = True

    lineno = 1
    while 1:
        try:

            if interactive is True:
                print(f"{fcmd.rdir} flipper> ", end="")
                argv = shlex.split(input(), comments=True, posix=True)
                if argv is None or len(argv) == 0:
                    print()
                    continue

            lineno += 1
            fcmd.run_comm(argv)

        except (EOFError, fcmd.QuitException, KeyboardInterrupt) as _e:
            interactive = False
            print(_e)
            break
        except cmdException as e:
            print("cmdException", e)
        except Exception as e:
            print(f"Exception: {e}")
            raise
        # finally:

        if interactive is not True:
            break


if __name__ == '__main__':
    main()
