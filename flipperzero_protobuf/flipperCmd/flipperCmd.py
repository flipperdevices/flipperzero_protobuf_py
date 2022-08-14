#!/usr/bin/env python3

""" command funtions and methods for command line app.

FlipperCMD

"""
# Written By: Peter Shipley github.com/evilpete
#
#  From python flipperzero_protobuf pkg

# ppylint: disable=line-too-long, no-member, too-many-branches, unused-import, unused-argument

import os
import sys
import readline
import zipfile
import time
# import pprint


# from google.protobuf.json_format import MessageToDict
from ..flipper_base import cmdException    # FlipperProtoBase
# from .flipper_storage import FlipperProtoStorage
from ..flipper_proto import FlipperProto
from ..cli_helpers import print_screen, flipper_tree_walk, calc_file_md5, calc_n_print_du, dict2datetime

_DEBUG = 0


#
# the docstring for class methods should be in the form of
# description on first line then syntax on the seconds line o
#
#         """display disk usage statistic
#         du <fipper_dir>
#         """
#
#

class FlipperCMD:
    # pylint: disable=too-many-instance-attributes

    class QuitException(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)

    def __init__(self, proto=None, **kwargs):

        self.debug = kwargs.get('debug', _DEBUG)

        if proto is None:
            serial_port = kwargs.get('serial_port', None)
            self.flip = FlipperProto(serial_port=serial_port, debug=self.debug)

        self._cmd_table = {}
        self._gen_cmd_table()

        self.rdir = '/ext'
        self.prevError = 'OK'
        self._local_time = time.localtime()
        self.color_ls = False

        self.verbose = kwargs.get('verbose', 0)

        self.excludes = [".thumbs", ".AppleDouble", ".RECYCLER", ".Spotlight-V100", '__pycache__']

    def _gen_cmd_table(self):
        """_gen_cmd_table doc"""

        # has to be in method to referance itself
        self.cmd_set = {
            ("LS", "LIST"): self.do_list,
            ("RM", "DEL", "DELETE"): self.do_del,
            # ("RM-TREE", "DEL-TRE", "DELTREE"): self.do_del,
            ("MV", "RENAME"): self.do_rename,
            ('DU', 'DISK-USAGE'): self._do_disk_usage,
            ("MD", "MKDIR"): self.do_mkdir,
            ("MD5SUM", "MD5"): self.do_md5sum,
            ("CAT",): self.do_cat_file,
            ("GET", "GETFILE"): self.do_get_file,
            ("GET-TREE", "GETTREE"): self.do_get_tree,
            ("PUT", "PUTFILE"): self.do_put_file,
            ("PUT-TREE", "PUTTREE"): self.do_put_tree,
            ("STAT",): self.do_stat,
            ("SET",): self._set_opt,
            ("TIME",): self.do_time,
            ("DF", "INFO"): self.do_info,
            ("DEV-INFO",): self.do_devinfo,
            # ("CD", "CHDIR", "!CD", "!CHDIR"): self.do_chdir,
            ("LCD", "LCHDIR"): self._do_chdir,
            ("LPWD",): self._do_print_cwd,
            ("PRINT-SCREEN",): self.do_print_screen,
            ("CD", "CHDIR", "RCD"): self._set_rdir,
            # ("PWD",):,
            ("HISTORY", "HIST"): self._print_cmd_hist,
            ("STOP-SESSION",): self.do_stop_session,
            ("START-SESSION",): self.do_start_session,
            ("SEND", "SEND-COMMAND"): self._do_send_cmd,
            ("REBOOT",): self.do_reboot,
            ("QUIT", "EXIT"): self.do_quit,
            ("ZIP",): self._do_zip,
            ("HELP", "?"): self.print_cmd_help,
        }

        for k, v in self.cmd_set.items():
            # print(f"len {type(k)} k{len(k)} {k}")
            for c in k:
                self._cmd_table[c] = v

    def get_cmd_keys(self) -> list:
        """returns list of commands"""
        return self._cmd_table.keys()

    def run_comm(self, argv) -> None:
        """run command line"""
        cmd = argv.pop(0).upper()

        if cmd in self._cmd_table:

            # handle help here insteqd of everywhere else
            if argv and argv[0] == '?':
                print("==")
                print(self._get_cmd_syntax(cmd))
                return

            self._cmd_table[cmd](cmd, argv)
        else:
            print("Unknown command : ", cmd)  # str(" ").join(argv)

    def do_quit(self, cmd, argv):   # pylint: disable=unused-argument
        """Exit Program
        QUIT
        """
        raise self.QuitException("Quit interactive mode")

    def _do_print_cwd(self, cmd, argv):   # pylint: disable=unused-argument
        """print local working directory
        LPWD
        """
        print(os.getcwd())

    def do_cmd_help(self, cmd, argv):    # pylint: disable=unused-argument
        """print command list"""
        self.print_cmd_help(cmd, argv)

    # prints first line of __doc__ string
    def print_cmd_help(self, cmd, argv):   # pylint: disable=unused-argument
        """print command list"""

        if argv and argv[0].upper() in self._cmd_table:
            hcmd = argv[0].upper()
            if self._cmd_table[hcmd].__doc__:
                hlist = self._cmd_table[hcmd].__doc__.split('\n')
                print(hlist[0])
                print("\t", hlist[1].strip())
                return

        for k, v in sorted(self.cmd_set.items()):
            if v.__doc__:
                print(f" {' '.join(k):<20s}:", v.__doc__.split('\n')[0].strip())

    def _get_cmd_syntax(self, cmdname):
        if cmdname in self._cmd_table and self._cmd_table[cmdname].__doc__:
            ret = self._cmd_table[cmdname].__doc__.split('\n')[1].rstrip()
        else:
            ret = cmdname

        return ret

    def _print_cmd_hist(self, cmd, argv):
        """Print command history
            history [count]
        """

        show_count = 20

        if argv:
            if argv[0].upper() in ['?', 'HELP']:
                raise cmdException(f"Syntax:\n\t{cmd} [count]\n"
                                   "\tprint command history")

            if argv[0].lstrip('-').isdigit():
                show_count = int(argv[0].lstrip('-'))

        start_at = readline.get_current_history_length() - show_count
        # print(f"{start_at} = {readline.get_current_history_length()} - {show_count}")
        start_at = max(start_at, 0)

        # print(f"show_count={show_count} start_at={start_at}")
        # for hist in self.cmdHistory[start_at:]:
        #    print(f"   {hist}")

        for i in range(start_at, readline.get_current_history_length()):
            print(str(readline.get_history_item(i + 1)))

    def do_devinfo(self, cmd, argv):  # pylint: disable=unused-argument
        """print device info
        Dev-Info
        """
        if argv and argv[0] in self.flip.device_info:
            print(f"{argv[0]:<25s} = {self.flip.device_info[argv[0]]}")
            return

        for k, v in sorted(self.flip.device_info.items()):
            print(f"{k:<25s} = {v}")

    def _interpret_val(self, opt):
        opt = opt.upper()

        if opt in ["ON", "TRUE", "T", "YES", "Y", "1"]:
            return 1

        if opt in ["OFF", "FALSE", "F", "NO", "Y", "0"]:
            return 0

        if opt.isdigit():
            return int(opt)

        return None

    def _set_opt(self, cmd, argv):     # pylint: disable=unused-argument
        """set or print current option value
        SET [Key Value]
        """
        if len(argv) < 2:
            excl = ' '.join(self.excludes)
            print(f"\tverbose:\t{self.verbose}\n"
                  f"\tdebug:  \t{self.debug}\n"
                  f"\tColor:    \t{self.color_ls}\n"
                  f"\tremote-dir:\t{self.rdir}\n"
                  f"\tPort:   \t{self.flip.port()}\n"
                  f"\texcludes: \t{excl}\n"
                  f"\tCWD:    \t{os.getcwd()}\n")
            return

        # print(f"set_opt {argv[0].upper()}")
        if argv[0].upper() == "COLOR":
            val = self._interpret_val(argv[1])
            if val is not None:
                self.color_ls = val
            return

        if argv[0].upper() == "DEBUG":
            val = self._interpret_val(argv[1])
            if val is not None:
                self.debug = val
            return

        if argv[0].upper() == "EXCLUDES":
            self.excludes = argv[1:]
            return

        if argv[0].upper() == "REMOTE-DIR":
            self._set_rdir(argv[0], argv[1:])
            return

        if argv[0].upper() == "VERBOSE":
            val = self._interpret_val(argv[1])
            if val is not None:
                self.verbose = val
            return

        raise cmdException(f"{cmd}: {argv[0]}: value not recognised")

    def do_time(self, cmd, argv):    # pylint: disable=unused-argument
        """Set or Get Current time from Flipper
        time [SET]
        """
        set_time = False
        if argv:
            if argv[0].upper() in ['SET', 'SET-TIME']:
                set_time = True
            else:
                print(f"Unknown Arg/Option: {argv[0]}")
                # raise cmdException(f"Syntax:\n\t{cmd} [SET]\n"
                #                    "\tdisplay time")

        if set_time:
            # system time used it called without arg
            self.flip.rpc_set_datetime()

        dtime_resp = self.flip.rpc_get_datetime()

        dt = dict2datetime(dtime_resp)
        print(dt.ctime())

    def _remote_path(self, path) -> str:
        if path.startswith('/'):
            return path

        return os.path.normpath(self.rdir + '/' + path)

    def _do_disk_usage(self, cmd, argv):
        """display disk usage statistic
        DU <fipper_dir>
        """
        if (not argv or argv[0] == '?'):
            raise cmdException(f"Syntax:\n\t{cmd} <DIR>\n"
                               "\tdisplay disk usage")

        targ = self._remote_path(argv.pop(0))

        calc_n_print_du(self.flip, targ)

    def _do_zip(self, cmd, argv):
        """Generate Zip Archive
        ZIP <zipfile> <fipper_dir>
        """
        if (not argv or argv[0] == '?' or len(argv) < 2):
            raise cmdException(f"Syntax:\n\t{cmd} <zipfile> <DIR>\n"
                               "\tGenerate Zip Archive")

        zipfilename = argv.pop(0)
        if not zipfilename.endswith((".zip", ".ZIP")):
            zipfilename = zipfilename + ".zip"

        self._local_time = time.localtime()
        with zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED) as zf:

            for targ in argv:

                targ = self._remote_path(targ)

                # pylint: disable=protected-access
                targ_stat = self.flip._rpc_stat(targ)

                if targ_stat is None:
                    print(f"{targ}: Not found")
                    continue

                if targ_stat['type'] != 'DIR':
                    self._zip_add_file(zf, targ)
                    continue

                for ROOT, DIRS, FILES in flipper_tree_walk(targ, self.flip):
                    for d in DIRS:
                        fpath = f"{ROOT}/{d}/"
                        print(f"zip: adding {fpath}")
                        zfi = zipfile.ZipInfo(fpath)
                        zfi.compress_type = zipfile.ZIP_STORED
                        zfi.external_attr = (0o040755 << 16) | 0x10
                        zf.writestr(zfi, '')

                    for f in FILES:
                        fpath = f"{ROOT}/{f}"
                        self._zip_add_file(zf, fpath)

    def _zip_add_file(self, zf, fpath):
        print(f"zip: adding {fpath}")
        file_data = self.flip.rpc_read(fpath)
        zfi = zipfile.ZipInfo(fpath)
        zfi.date_time = self._local_time[:6]
        zfi.compress_type = zipfile.ZIP_STORED
        zfi.external_attr = (0o0644 << 16)
        zf.writestr(zfi, file_data)

    def _do_send_cmd(self, cmd, argv):  # pylint: disable=unused-argument
        """Semd non rpc command to flipper
        SEND <command string>
        """
        cmd_str = " ".join(argv)
        self.flip.send_cmd(cmd_str)

    # pylint: disable=protected-access
    def _set_rdir(self, cmd, argv) -> None:
        """change current directory on flipper
           cd <DIR>\n
        """
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax:\n\t{cmd} <DIR>\n"
                               "\tset remote directory")

        remdir = argv.pop(0)

        if remdir.startswith('/'):
            newdir = remdir
        else:
            newdir = os.path.normpath(self.rdir + '/' + remdir)

        if newdir in ['/', '/ext', '/int']:
            self.rdir = newdir
            print(f"Remote directory: {newdir}")

        stat_resp = self.flip._rpc_stat(newdir)

        # if self.debug:
        #     print(f"{cmd}:\n\tremdir={remdir}\n\tnewdir={newdir}\ni\tstat_resp={stat_resp}")

        if stat_resp is None:
            print(f"{newdir}: Not found")
        elif stat_resp['type'] == 'DIR':
            self.rdir = newdir
        else:
            print("{newdir}: not a directory")

        print(f"Remote directory: {newdir}")

    def do_print_screen(self, cmd, argv):
        """Take screendump in ascii or PBM format
            PRINT-SCREEN [filename.pbm]
        """
        outf = None
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax:\n\t{cmd} [filename.pbm]\n"
                               "\tfile has to end in .pbm\n"
                               "\tif no file is given image is printed to stdout")

        if argv:
            outf = argv.pop(0)
        print_screen(self.flip.rpc_gui_snapshot_screen(), outf)

    # storage_pb2.File.DIR == 1
    # storage_pb2.File.FILE == 0
    # Colors
    @staticmethod
    def pink(t):
        return f'\033[95m{t}\033[0m'

    @staticmethod
    def blue(t):
        return f'\033[94m{t}\033[0m'
    # def magenta(t):  return f'\033[93m{t}\033[0m'
    # def yellow(t):  return f'\033[93m{t}\033[0m'
    # def green(t):   return f'\033[92m{t}\033[0m'
    # def red(t):     return f'\033[91m{t}\033[0m'

    def do_list(self, cmd, argv):
        """list files and dirs on Flipper device
        ls [-l] [-m] <flipper_directory>
        """
        # pylint: disable=protected-access,too-many-branches

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

        flist = self.flip.rpc_storage_list(targ)
        flist.sort(key=lambda x: (x['type'], x['name'].lower()))

        # if self.debug:
        #     print("Storage List result: ", targ)

        # should split off file list printing into sub func
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
                        md5val = self.flip.rpc_md5sum(targ + '/' + line['name'])
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
                    if self.color_ls:
                        name = self.blue(line['name'])
                    else:
                        name = line['name'] + '/'           # ("-" if line['type'] == 'DIR' else "+" )
                else:
                    if self.color_ls:
                        name = self.pink(line['name'])
                    else:
                        name = line['name']

                if j % 4 == 1:
                    endl = '\n'

                print(f"{name:<35s}", end=endl)

        # add blank line
        print()

    def do_del(self, cmd, argv):
        """delete file of directory on flipper device
        DEL [-r] <file>
        """
        error_str = f"Syntax :\n\t{cmd} [-r] file"
        # if not argv or argv[0] == '?':
        #     raise cmdException(error_str)

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

        if self.verbose:
            print(f"{cmd} {'-r' if recursive else ''} {targ}")

        self.flip.rpc_delete(targ, recursive=recursive)

    def do_rename(self, cmd, argv):
        """rename file or dir
            RENAME <old_name> <new_name>
            renames or move file on flipper device
        """
        if (len(argv) > 1 and argv[0] != "?"):
            old_fn = argv.pop(0)
            new_fn = argv.pop(0)

            if not old_fn.startswith('/'):
                old_fn = os.path.normpath(self.rdir + '/' + old_fn)

            if not new_fn.startswith('/'):
                new_fn = os.path.normpath(self.rdir + '/' + new_fn)

            # flipper does not line the trailing '/'
            new_fn = new_fn.rstrip('/')
            old_fn = old_fn.rstrip('/')

            # is destination a directory?
            stat_resp = self.flip._rpc_stat(new_fn)
            if stat_resp is not None and stat_resp.get('type', "") == 'DIR':
                bname = os.path.basename(old_fn)
                new_fn = f"{new_fn}/{bname}"

            if self.debug:
                print(cmd, old_fn, new_fn)

            self.flip.rpc_rename_file(old_fn, new_fn)

        else:
            raise cmdException(f"Syntax :\n\t{cmd} <old_name> <new_name>")

    def _mkdir_path(self, targ):
        """Simplified mkdir for internal use"""

        subpath = ""
        for p in targ.split('/'):
            if not p:
                continue

            subpath = subpath + '/' + p
            self.flip._mkdir_path(subpath)

    def do_mkdir(self, cmd, argv):
        """Create a new directory
            MKDIR <directory>
            Make directories on flipper device
        """
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} <directory>")

        targ = argv.pop(0)
        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        self.flip.rpc_mkdir(targ)

    def _do_chdir(self, cmd, argv):
        """Change local current directory
        LCD  <directory>
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
        """md5 hash of the file
        MD5 <flipper_file>
        """
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

        if self.debug:
            print(cmd, targ)

        md5sum_resp = self.flip.rpc_md5sum(targ)
        print(f"md5sum_resp={md5sum_resp}")

    def do_cat_file(self, cmd, argv):
        """read flipper file to screen
        cat <flipper_file>
        """
        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        remote_filen = argv.pop(0)

        if not remote_filen.startswith('/'):
            remote_filen = os.path.normpath(self.rdir + '/' + remote_filen)

        if self.debug:
            print(cmd, remote_filen)

        read_resp = self.flip.rpc_read(remote_filen)
        # print("cmd_read {len(read_resp)}")
        print(read_resp.decode('utf-8'))

    def _get_file(self, remote_filen, local_filen):
        """Simplified get file for internal use"""
        file_data = self.flip.rpc_read(remote_filen)
        with open(local_filen, 'wb') as fd:
            fd.write(file_data)

    def do_get_file(self, cmd, argv):
        """copy file from flipper
        GET <flipper_file> <local_filename>
        """
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

            # is destination a directory?
            if os.path.isdir(local_filen):
                bname = os.path.basename(remote_filen)
                local_filen = local_filen + '/' + bname

            if self.debug:
                print(cmd, remote_filen, local_filen)

            # if self.verbose:
            print(f"get {remote_filen} -> {local_filen}\n")

            # _get_file(remote_filen, local_filen)

            file_data = self.flip.rpc_read(remote_filen)
            # print(f"getting {len(file_data)} bytes")
            with open(local_filen, 'wb') as fd:
                fd.write(file_data)
        else:
            raise cmdException(f"Syntax :\n\t{cmd} <remote_filename> <local_filename>")

    def _put_file(self, local_filen, remote_filen):
        """Simplified put file """
        with open(local_filen, 'rb') as fd:
            file_data = fd.read()

        self.flip.rpc_write(remote_filen, file_data)

    def do_put_file(self, cmd, argv):
        """copy file to flipper
        PUT  <local_filename> <flipper_file>
        """
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

        # is destination a directory?
        stat_resp = self.flip._rpc_stat(remote_filen)
        if stat_resp is not None and stat_resp.get('type', "") == 'DIR':
            bname = os.path.basename(local_filen)
            remote_filen = remote_filen + '/' + bname

        # print(cmd, local_filen, remote_filen)

        if self.verbose:
            print(f"copy {local_filen} -> {remote_filen}")

        # _put_file(local_filen, remote_filen)

        with open(local_filen, 'rb') as fd:
            file_data = fd.read()

        # print(f"putting {len(file_data)} bytes")
        self.flip.rpc_write(remote_filen, file_data)

    # this needs code to act like cp/rsync were if source_file ends in a /,
    # the contents of the directory are copied rather than the directory itself
    def do_put_tree(self, cmd, argv):
        # pylint: disable=protected-access,too-many-branches
        """copy directory tree to flipper
        PUT-TREE  <local_directort> <flipper_directory>
        If the source_file ends in a /, the contents of
        the directory are copied rather than the directory itself.
        """
        # excludes = [".thumbs", ".AppleDouble", ".RECYCLER", ".Spotlight-V100", '__pycache__']
        check_md5 = False

        verbose = self.debug or self.verbose

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
        stat_resp = self.flip._rpc_stat(remote_dir)

        if stat_resp is not None and stat_resp.get('type', "") == 'FILE':
            raise cmdException(f"{syntax_str}\n\t{remote_dir}: exists as a file")

        if verbose:
            print(f"{cmd} '{local_dir_full}' '{remote_dir}")

        local_dir_len = len(local_dir_full)
        for ROOT, dirs, FILES in os.walk(local_dir_full, topdown=True):
            dirs[:] = [de for de in dirs if de not in self.excludes and de[0] != '.' and '+' not in de]
            FILES[:] = [de for de in FILES if de not in self.excludes and de[0] != '.']

            dt = ROOT[local_dir_len:]

            remdir = os.path.normpath(remote_dir + '/' + dt)

            for d in dirs:
                if verbose:
                    print(f"mkdir {remdir}/{d}")
                self._mkdir_path(f"{remdir}/{d}")
            for f in FILES:
                # if not f.isalnum() or '+' in f:
                #    continue
                if verbose:
                    print(f"copy {ROOT} / {f} -> {remdir} / {f}")
                try:
                    self._put_file(f"{ROOT}/{f}", f"{remdir}/{f}")
                except cmdException as _e:
                    # if self.debug:
                    #     print(f"{remdir}/{f} : {e} : SKIPPING")
                    continue
                # t_size += os.path.getsize(f"{ROOT}/{f}")

                if check_md5:
                    hash1 = calc_file_md5(f"{ROOT}/{f}")
                    hash2 = self.flip.rpc_md5sum(f"{remdir}/{f}")
                    if hash2 != hash1:
                        print("MD5 mismatch: {remdir}/{f}")
                        print(f"{hash1} <-> {hash2}")

            # print(f"Total: {t_size}")

    # this needs code to act like cp/rsync were if source_file ends in a /,
    # the contents of the directory are copied rather than the directory itself
    def do_get_tree(self, cmd, argv):
        """copy directory tree from flipper
        GET-TREE   <flipper_directory> <local_directort>
        If the source_file ends in a /, the contents of
        the directory are copied rather than the directory itself.
        """

        verbose = self.debug or self.verbose

        syntax_str = f"Syntax :\n\t{cmd} <local_directory> <remote_destination>"
        if (len(argv) < 1 or argv[0] in ["?", "help"]):
            raise cmdException(syntax_str)

        #  add more logic here like with put-tree
        remote_dir = argv.pop(0)

        if argv:
            local_dir = argv.pop(0)
        else:
            local_dir = '.'

        if verbose:
            print(f"{cmd} '{remote_dir}' '{local_dir}'")

        if not remote_dir.startswith('/'):
            remote_dir_full = os.path.normpath(self.rdir + '/' + remote_dir)
        else:
            remote_dir_full = remote_dir

        if verbose:
            print(f"'{remote_dir}' -> '{remote_dir_full}'")

        stat_resp = self.flip._rpc_stat(remote_dir_full)
        if stat_resp is None or stat_resp.get('type', "") == 'FILE':
            raise cmdException(f"{syntax_str}\n\t{remote_dir}: is a file, expected directory")

        if os.path.isdir(local_dir) and not remote_dir.endswith('/'):
            local_dir = local_dir + '/' + os.path.basename(remote_dir_full)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
        else:
            os.makedirs(local_dir)

        if verbose:
            print(f"{cmd} '{remote_dir_full}' '{os.path.abspath(local_dir)}'")

        remote_dir_len = len(remote_dir_full)
        for ROOT, dirs, FILES in flipper_tree_walk(remote_dir_full, self.flip):
            dirs[:] = [de for de in dirs if de not in self.excludes]

            dt = ROOT[remote_dir_len:]
            locdir = os.path.normpath(local_dir + '/' + dt)

            for d in dirs:
                if verbose:
                    print(f"mkdir {locdir} / {d}")
                os.makedirs(f"{locdir}/{d}")

            for f in FILES:
                if verbose:
                    print(f"copy {ROOT} / {f} -> {locdir} / {f}")
                self._get_file(f"{ROOT}/{f}", f"{locdir}/{f}")

    def do_info(self, _cmd, argv):
        """get Filesystem info
            INFO [filesystem]
        """

        targfs = ['/ext', '/int']

        if len(argv) > 0:
            targ = argv.pop(0)

            if not targ.startswith('/'):
                targ = os.path.normpath(self.rdir + '/' + targ)
            targfs = [targ]

        for t in targfs:
            info_resp = self.flip.rpc_info(t)

            tspace = int(info_resp['totalSpace'])
            fspace = int(info_resp['freeSpace'])
            print(f"\nfilesystem: {t}\n"
                  f"  totalSpace: {tspace}\n"
                  f"  freeSpace:  {fspace}\n"
                  f"  usedspace:  {tspace - fspace}")
        print()

    def do_stat(self, cmd, argv):
        """get info about file or directory
        Stat <flipper_file>
        """

        if (len(argv) == 0 or argv[0] == '?' or len(argv) > 1):
            raise cmdException(f"Syntax :\n\t{cmd} file")

        targ = argv.pop(0)

        if not targ.startswith('/'):
            targ = os.path.normpath(self.rdir + '/' + targ)

        targ = targ.rstrip('/')

        if self.debug:
            print(cmd, targ)

        stat_resp = self.flip.rpc_stat(targ)

        if self.debug:
            print(f"stat_resp={stat_resp}")

        # if stat_resp.get('commandId', 0) != 0:
        #    print(f"Error: {stat_resp['commandStatus']}")
        #    return

        if stat_resp.get('type', "") == 'DIR':
            print(f"{targ:<25s}\t   DIR")
        else:
            print(f"{targ:<25s}\t{stat_resp['size']:>6d}")

    def do_start_session(self, cmd, argv):   # pylint: disable=unused-argument
        """(re) start RPC session
        START-SESSION
        """
        self.flip.start_rpc_session()

    def do_stop_session(self, cmd, argv):     # pylint: disable=unused-argument
        """stop RPC session
        STOP-SESSION
        """
        self.flip.rpc_stop_session()

    def do_reboot(self, cmd, argv):
        """reboot flipper
            REBOOT [MODE]
            MODE can be 'OS', 'DFU' or 'UPDATE'
        """

        if (len(argv) < 1 or argv[0] == "?"):
            raise cmdException(f"Syntax :\n\t{cmd} [OS | DFU | UPDATE]")

        mode = argv.pop(0)

        if mode not in ['OS', 'DFU', 'UPDATE']:
            raise cmdException(f"Syntax :\n\t{cmd} [OS | DFU | UPDATE]")

        self.flip.rpc_reboot(mode)

        # quit if not booting into OS mode
        if mode in ['DFU', 'UPDATE']:
            self.QuitException(f"REBOOT {mode}")


#
# Do nothing
# (syntax check)
#
if __name__ == "__main__":
    import __main__
    print(__main__.__file__)

    print("syntax ok")
    sys.exit(0)
