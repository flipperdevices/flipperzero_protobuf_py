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
from .cli_helpers import print_screen, flipper_tree_walk, calc_file_md5

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
    "PUT-TREE": "copy directory tree to flipper",

    "GET, GETFILE": "copy file from flipper",
    "GET-TREE": "copy directory tree from flipper",

    "CAT": "read file to screen",

    "PRINT-SCREEN": "screendump in ascii or PBM format",

    "RCD, RCHDIR": "change current directory on flipper",

    "HISTORY": "print command History",

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

    def __init__(self, proto=None, debug=_DEBUG, verbose=0):

        if proto is None:
            self.flip = FlipperProto()

        self.rdir = '/ext'
        self.prevError = 'OK'
        # self.cmdHistory = []

        # for i in range(50):
        #    self.cmdHistory.append( f"history {i}")

        self.debug = debug
        self.flip._debug = self.debug
        self.verbose = verbose

    # TODO:  Convert this into a dict lookup
    def run_comm(self, argv):

        # self.cmdHistory.append(" ".join(argv))
        # print(f"hist len={len(self.cmdHistory)}")

        cmd = argv.pop(0).upper()

        if cmd in ["LS", "LIST"]:
            self.do_list(cmd, argv)

        elif cmd in ["RM", "DEL", "DELETE"]:
            self.do_del(cmd, argv)

        elif cmd in ["RM-TREE", "DEL-TRE", "DELTREE"]:
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

        elif cmd in ["GET-TREE", "GETTREE"]:
            self.do_get_tree(cmd, argv)

        elif cmd in ["PUT", "PUTFILE"]:
            self.do_put_file(cmd, argv)

        elif cmd in ["PUT-TREE", "PUTTREE"]:
            self.do_put_tree(cmd, argv)

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

        elif cmd in ["RCD", "RCHDIR"]:
            print(self.rdir)

        # elif cmd in ["RPWD", "RWD"]:

        elif cmd in ["HISTORY", "HIST"]:
            self.print_cmd_hist(cmd, argv)

        elif cmd in ["DEBUG", "SET-DEBUG", "GET=DEBUG"]:
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

    def print_cmd_hist(self, cmd, argv):

        show_count = 20

        if argv:
            if argv[0].upper() in ['?', 'HELP']:
                raise cmdException(f"Syntax :\n\t{cmd} [count]\n"
                                   "\tprint command history")

            if argv[0].lstrip('-').isdigit():
                show_count = int(argv[0].lstrip('-'))

        # show_count = show_count * -1

        start_at = readline.get_current_history_length() - show_count
        print(f"{start_at} = {readline.get_current_history_length()} - {show_count}")
        start_at = max(start_at, 0)

        print(f"show_count={show_count} start_at={start_at}")
        # for hist in self.cmdHistory[start_at:]:
        #    print(f"   {hist}")

        for i in range(start_at, readline.get_current_history_length()):
            print(str(readline.get_history_item(i + 1)))

    # pylint: disable=protected-access
    def set_debug(self, cmd, argv):
        """
            DEBUG: [DEBUG_LEVEL]\n"
                  "\tshows current level if no arg is given")
        """
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

        self.flip._debug = self.debug

    # pylint: disable=protected-access
    def set_rdir(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} <DIR>\n"
                               "\tset remote directory")

        remdir = argv.pop(0)

        if remdir.startswith('/'):
            newdir = remdir
        else:
            newdir = os.path.normpath(self.rdir + '/' + remdir)

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
            targ = os.path.normpath(self.rdir + '/' + targ)

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
        """ DEL <file>
        Delete file of directory on flipper device
        """
        error_str = f"Syntax :\n\t{cmd} file"
        if not argv or argv[0] == '?':
            raise cmdException(error_str)

        recursive = False
        if argv and argv[0] in ['-r', '-R']:
            argv.pop(0)
            recursive = True

        if argv:
            targ = argv.pop(0).rstrip('/')
        else:
            raise cmdException(error_str)

        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

        self.flip.cmd_delete(targ, recursive=recursive)

    def do_rename(self, cmd, argv):
        """ RENAME <old_name> <new_name>
            renames or move file on flipper device
        """
        if (len(argv) > 1 and argv[0] != "?"):
            old_fn = argv.pop(0)
            new_fn = argv.pop(0)

            if not old_fn.startswith('/'):
                old_fn = os.path.normpath(self.rdir + '/' + old_fn)

            if not new_fn.startswith('/'):
                new_fn = os.path.normpath(self.rdir + '/' + new_fn)

            if self.debug:
                print(cmd, old_fn, new_fn)

            rename_resp = self.flip.cmd_rename_file(old_fn, new_fn)

            if self.debug:
                print(f"rename_resp={rename_resp}")

        else:
            raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")

    def _mkdir_path(self, targ):
        """Simplified mkdir"""

        subpath = ""
        for p in targ.split('/'):
            if not p:
                continue

            subpath = subpath + '/' + p
            self.flip._mkdir_path(subpath)

    def do_mkdir(self, cmd, argv):
        """
            MKDIR <directory>
            Make directories on flipper device
        """
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)
        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        self.flip.cmd_mkdir(targ)

    def do_chdir(self, cmd, argv):
        """
            CD  <directory>
            Change local current directory
        """
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
            targ = os.path.normpath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        md5sum_resp = self.flip.cmd_md5sum(targ)
        print(f"md5sum_resp={md5sum_resp}")

    def do_cat_file(self, cmd, argv):
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        remote_filen = argv.pop(0)

        if not remote_filen.startswith('/'):
            remote_filen = os.path.normpath(self.rdir + '/' + remote_filen)

        if self.debug:
            print(cmd, remote_filen)

        read_resp = self.flip.cmd_read(remote_filen)
        # print("cmd_read {len(read_resp)}")
        print(read_resp)

    def _get_file(self, remote_filen, local_filen):
        file_data = self.flip.cmd_read(remote_filen)
        with open(local_filen, 'wb') as fd:
            fd.write(file_data)

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
                remote_filen = os.path.normpath(self.rdir + '/' + remote_filen)

            if self.debug:
                print(cmd, remote_filen, local_filen)

            file_data = self.flip.cmd_read(remote_filen)
            # print(f"getting {len(file_data)} bytes")
            with open(local_filen, 'wb') as fd:
                fd.write(file_data)
        else:
            raise cmdException(f"Syntax :\n\t{cmd} <remote_filename> <local_filename>")

    def _put_file(self, local_filen, remote_filen):
        """Simplified put file """
        with open(local_filen, 'rb') as fd:
            file_data = fd.read()

        self.flip.cmd_write(remote_filen, file_data)

    def do_put_file(self, cmd, argv):
        if (len(argv) < 1 or argv[0] == "?"):
            raise cmdException(f"Syntax :\n\t{cmd} <local_file> <remote_file_or_dir>")

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
            remote_filen = os.path.normpath(self.rdir + '/' + remote_filen)

        stat_resp = self.flip._cmd_stat(remote_filen)
        # print("stat_resp=", stat_resp)
        if stat_resp is not None and stat_resp.get('type', "") == 'DIR':
            remote_filen = remote_filen + '/' + local_filen

        # print(cmd, local_filen, remote_filen)

        with open(local_filen, 'rb') as fd:
            file_data = fd.read()

        print(f"putting {len(file_data)} bytes")
        self.flip.cmd_write(remote_filen, file_data)

    def do_put_tree(self, cmd, argv):

        excludes = [".thumbs", ".AppleDouble", ".RECYCLER", ".Spotlight-V100", '__pycache__']
        check_md5 = False

        syntax_str = f"Syntax :\n\t{cmd} [-md5] <local_directory> <remote_destination>"
        if (len(argv) < 2 or argv[0] in ["?", "help"]):
            raise cmdException(syntax_str)

        if (len(argv) > 2) and argv[0].upper() in ['-M', '-MD5']:
            argv.pop(0)
            check_md5 = True

        if len(argv) < 2:
            raise cmdException(syntax_str)
        local_dir = argv.pop(0)
        remote_dir = argv.pop(0)

        if not remote_dir.startswith('/'):
            remote_dir = os.path.normpath(self.rdir + '/' + remote_dir)

        if not os.path.isdir(local_dir):
            raise cmdException(f"{syntax_str}\n\t{local_dir}: not a directory")

        local_dir_full = os.path.abspath(local_dir)
        local_dir_targ = os.path.split(local_dir_full)[1]
        # remote_dir_targ = os.path.split(remote_dir)[1]

        # if local_dir.endswith('/') or local_dir_targ == remote_dir_targ:

        remote_dir = remote_dir + '/' + local_dir_targ
        stat_resp = self.flip._cmd_stat(remote_dir)

        if stat_resp is not None and stat_resp.get('type', "") == 'FILE':
            raise cmdException(f"{syntax_str}\n\t{remote_dir}: exists as a file")

        local_dir_len = len(local_dir_full)
        for ROOT, dirs, FILES in os.walk(local_dir_full, topdown=True):
            dirs[:] = [de for de in dirs if de not in excludes and de[0] != '.' and '+' not in de]
            FILES[:] = [de for de in FILES if de not in excludes and de[0] != '.']

            dt = ROOT[local_dir_len:]

            # print(f"\nROOT = {ROOT} {dt}")

            # t_size = 0

            remdir = os.path.normpath(remote_dir + '/' + dt)

            for d in dirs:
                if self.debug:
                    print(f"mkdir {remdir}/{d}")
                self._mkdir_path(f"{remdir}/{d}")
            for f in FILES:
                # if not f.isalnum() or '+' in f:
                #    continue
                if self.debug:
                    print(f"copy {ROOT} / {f} -> {remdir} / {f}")
                try:
                    self._put_file(f"{ROOT}/{f}", f"{remdir}/{f}")
                except cmdException as e:
                    print(f"{remdir}/{f} : {e} : SKIPPING")
                    continue
                # t_size += os.path.getsize(f"{ROOT}/{f}")

                if check_md5:
                    hash1 = calc_file_md5(f"{ROOT}/{f}")
                    hash2 = self.flip.cmd_md5sum(f"{remdir}/{f}")
                    if hash2 != hash1:
                        print("MD5 mismatch: {remdir}/{f}")
                        print(f"{hash1} <-> {hash2}")

            # print(f"Total: {t_size}")

    def do_get_tree(self, cmd, argv):

        syntax_str = f"Syntax :\n\t{cmd} <local_directory> <remote_destination>"
        remote_dir = argv.pop(0)
        local_dir = argv.pop(0)

        if not remote_dir.startswith('/'):
            remote_dir_full = os.path.normpath(self.rdir + '/' + remote_dir)
        else:
            remote_dir_full = remote_dir

        stat_resp = self.flip._cmd_stat(remote_dir_full)
        if stat_resp is None or stat_resp.get('type', "") == 'FILE':
            raise cmdException(f"{syntax_str}\n\t{remote_dir}: is a file, expected directory")

        remote_dir_len = len(remote_dir_full)
        for ROOT, dirs, FILES in flipper_tree_walk(remote_dir_full, self.flip):

            dt = ROOT[remote_dir_len:]
            locdir = os.path.normpath(local_dir + '/' + dt)

            for d in dirs:
                if self.debug:
                    print(f"mkdir {locdir} / {d}")
                os.makedirs(f"{locdir}/{d}")

            for f in FILES:
                if self.debug:
                    print(f"copy {ROOT} / {f} -> {locdir} / {f}")
                self._get_file(f"{ROOT}/{f}", f"{locdir}/{f}")

    def do_info(self, _cmd, argv):
        targ = '/ext'

        if len(argv) > 0:
            targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

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
            targ = os.path.normpath(self.rdir + '/' + targ)

        targ = targ.rstrip('/')

        if self.debug:
            print(cmd, targ)

        stat_resp = self.flip.cmd_stat(targ)

        if self.debug:
            print(f"stat_resp={stat_resp}")

        # if stat_resp.get('commandId', 0) != 0:
        #    print(f"Error: {stat_resp['commandStatus']}")
        #    return

        if stat_resp.get('type', "") == 'DIR':
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
                # print(f"{fcmd.rdir} flipper> ", end="")
                prompt = f"{fcmd.rdir} flipper> "
                argv = shlex.split(input(prompt), comments=True, posix=True)
                if argv is None or len(argv) == 0:
                    print()
                    continue

            lineno += 1
            fcmd.run_comm(argv)

        except (EOFError, fcmd.QuitException, KeyboardInterrupt) as _e:
            interactive = False
            # print(_e)
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
