#!/usr/bin/env python3
# ppylint: disable=line-too-long, no-member, too-many-branches, unused-import, unused-argument

# import os
# import sys
# import readline
import shlex
# import pprint
import argparse


from .flipperCmd import FlipperCMD
# from google.protobuf.json_format import MessageToDict
from .flipper_base import cmdException    # FlipperProtoBase
# from .flipper_storage import FlipperProtoStorage
# from .flipper_proto import FlipperProto
# from .cli_helpers import print_screen, flipper_tree_walk, calc_file_md5


def arg_opts():

    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', dest="verbose",
                        default=0,
                        help='Increase debug verbosity', action='count')

    parser.add_argument("-p", "--port", dest="serial_port",
                        default=None,
                        help="Serial Port")

    data_grp = parser.add_mutually_exclusive_group()

    data_grp.add_argument("-i", "--interactive", dest="interactive",
                          default=False, action='store_true',
                          help="Interactive Mode")

    data_grp.add_argument("-c", "--cmd-file", dest="cmd_file",
                          type=argparse.FileType('r', encoding='UTF-8'),
                          default=None,
                          help="Command File")

    return parser.parse_known_args()


def main():

    # global rdir
    interactive = False

    arg, u = arg_opts()

    fcmd = FlipperCMD(serial_port=arg.serial_port, verbose=arg.verbose)
    # proto = FlipperProto()

    # argv = sys.argv[1:]

    argv = u

    if len(argv) == 0 and arg.cmd_file is None:
        print("Entering interactive mode")
        print("Device Name :", fcmd.flip.device_info.get('hardware_name', "Unknown"))
        interactive = True

    lineno = 1
    while 1:
        try:

            if arg.cmd_file:
                for line in arg.cmd_file:
                    if fcmd.verbose or fcmd.debug:
                        print("cmd=", line)
                    argv = shlex.split(line, comments=True, posix=True)
                    fcmd.run_comm(argv)
                break

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
            print("")
            # print(_e)
            break

        except cmdException as e:
            print("Command Error", e)

        except ValueError as e:
            print("ValueError", e)
            if interactive:
                continue
            break

        except IOError as e:
            # do we need reconnect code ???
            print("IOError", e)
            if interactive:
                continue

        # except google.protobuf.message.DecodeError as e:

        except Exception as e:
            print(f"Exception: {e}")
            raise

        # finally:

        if interactive is not True or arg.cmd_file is not None:
            break


if __name__ == '__main__':
    main()
