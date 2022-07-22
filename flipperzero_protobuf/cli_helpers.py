#!/usr/bin/env python3

import datetime
import numpy

from .flipper_base import cmdException

def print_hex(bytes_data):
    # print("".join('{:02x} '.format(x) for x in bytes_data))
    print("".join(f'{x:02x} ') for x in bytes_data)

SCREEN_H = 128
SCREEN_W = 64


def print_screen(screen_bytes, dest=None):
    """
        convert screendump data into ascii or .pbm for format
    """
    dat = _dump_screen(screen_bytes)

    if dest is None:
        for y in range(0, SCREEN_W, 2):
            for x in range(1, SCREEN_H + 1):
                if int(dat[x][y]) == 1 and int(dat[x][y + 1]) == 1:
                    print('\u2588', end='')
                if int(dat[x][y]) == 0 and int(dat[x][y + 1]) == 1:
                    print('\u2584', end='')
                if int(dat[x][y]) == 1 and int(dat[x][y + 1]) == 0:
                    print('\u2580', end='')
                if int(dat[x][y]) == 0 and int(dat[x][y + 1]) == 0:
                    print(' ', end='')
            print()

    elif dest.endswith('.pbm'):
        with open(dest, "w", encoding="utf-8") as fd:
            print(f"P1\n{SCREEN_H + 1} {SCREEN_W}", file=fd)
            for y in range(0, SCREEN_W):
                print(numpy.array2string(dat[:, y], max_line_width=300)[1:-1], file=fd)
    else:
        raise cmdException("invalid filename")


def _dump_screen(screen_bytes):
    """
        get screendump data
    """
    # pylint: disable=multiple-statements

    def get_bin(x):
        return format(x, '08b')

    scr = numpy.zeros((SCREEN_H + 1, SCREEN_W + 1), dtype=int)
    data = screen_bytes

    x = y = 0
    basey = 0

    for i in range(0, int(SCREEN_H * SCREEN_W / 8)):
        tmp = get_bin(data[i])[::-1]

        y = basey
        x += 1
        for c in tmp:
            scr[x][y] = c
            y += 1

        if (i + 1) % SCREEN_H == 0:
            basey += 8
            x = 0

    return scr


def datetime2dict(dt=None):
    """
        convert datatime obj into type dict
    """

    if dt is None:
        dt = datetime.datetime.now()

    tlist = list(dt.timetuple())

    datetime_dict = {
        'year': tlist[0],
        'month': tlist[2],
        'day': tlist[3],
        'hour': tlist[4],
        'minute': tlist[5],
        'second': tlist[6],
        'weekday': tlist[7] + 1,
    }

    return datetime_dict


def dict2datetime(d):
    """
        convert type dict into datatime obj
    """
    tdict = d.copy()    # we dont want to destroy the caller's data
    del tdict['weekday']
    return datetime.datetime(**tdict)
