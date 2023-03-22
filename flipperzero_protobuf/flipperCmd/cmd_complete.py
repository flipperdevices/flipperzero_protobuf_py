"""
command Completion callback class for FlipperCMD interface.
"""

import readline
import sys
from os import environ

__all__ = ["Cmd_Complete"]


class Cmd_Complete:  # Custom completer
    """Command Completion callback class for FlipperCMD interface."""

    def __init__(self, **kwargs):
        self.volcab = kwargs.get("volcab", [])
        self.volcab.sort()

        # self.cmd_comp_key = []
        self.cmd_comp_cache = {}
        self.prompt = ">"

    def setup(self, volcab=None):
        """Command Completion setup callback."""

        if volcab:
            self.volcab = sorted(volcab)

        self.prompt = "Flipper>>"
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.cmd_complete)

        completer_delims = readline.get_completer_delims()
        completer_delims = completer_delims.replace("-", "")
        readline.set_completer_delims(completer_delims)

        # readline.set_completion_display_matches_hook(self.display_matches)

    def cmd_complete(self, text, state) -> list:
        """Command Completion callback hook."""

        # print(f"Call '{text}' {state}")
        buf = readline.get_line_buffer()
        # print(f"buf= >{buf}<")
        # print()
        # ct = readline.get_completion_type()
        # print(f"ct={ct}\n\n")

        # if buf.endswith('?'):
        #     print help syntax

        # only do completion for first word
        if buf and buf[-1] == " " and buf.strip().upper() in self.volcab:
            return [None]

        text = text.upper()
        if text in self.cmd_comp_cache:
            # print(f"Cache {text} {state}", self.cmd_comp_cache[text])
            return self.cmd_comp_cache[text][state]

        results = [x for x in self.volcab if x.startswith(text)] + [None]
        self.cmd_comp_cache[text] = results
        return results[state]

        # https://stackoverflow.com/questions/20625642/autocomplete-with-readline-in-python3

    def display_matches(self, _substitution, matches, _longest_match_length):
        """Command Completion display callback hook."""
        # line_buffer = readline.get_line_buffer()
        columns = environ.get("COLUMNS", 80)

        tpl = "{:<" + str(int(_longest_match_length * 1.2)) + "}"

        # print(f"substitution={substitution}")
        # print(f"matches={matches}")
        # print(f"_longest_match_length={_longest_match_length}")
        # print(f"tpl={tpl}")

        buffer = ""
        for match in matches:
            match = tpl.format(match)
            if len(buffer + match) > columns:
                print(buffer)
                buffer = ""
            buffer += match

        print(self.prompt.rstrip(), readline.get_line_buffer(), sep="", end="")

        sys.stdout.flush()
