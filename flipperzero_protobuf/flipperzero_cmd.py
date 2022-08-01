#!/usr/bin/env python3
# ppylint: disable=line-too-long, no-member, too-many-branches, unused-import, unused-argument

# import os
import sys
# import readline
import shlex
# import pprint


from .flipperCmd import FlipperCMD
# from google.protobuf.json_format import MessageToDict
from .flipper_base import cmdException    # FlipperProtoBase
# from .flipper_storage import FlipperProtoStorage
# from .flipper_proto import FlipperProto
# from .cli_helpers import print_screen, flipper_tree_walk, calc_file_md5


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

        except ValueError:
            print("ValueError", e)
            if interactive:
                continue

            break

        # except google.protobuf.message.DecodeError as e:

        except Exception as e:
            print(f"Exception: {e}")
            raise

        # finally:

        if interactive is not True:
            break


if __name__ == '__main__':
    main()
