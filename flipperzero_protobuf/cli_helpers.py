#!/usr/bin/env python3

import datetime
import hashlib
import numpy

from .flipper_base import cmdException


def print_hex(bytes_data):
    print("".join(f'{x:02x} ' for x in bytes_data))


SCREEN_H = 128
SCREEN_W = 64


def calc_file_md5(fname):
    """Calculate md5 hash for file

    Parameters
    ----------
        fname : str
            path to local fole

    Returns
    -------
        str containing md5 message-digest fingerprint for file

    """
    with open(fname, 'rb') as fd:
        hsum = hashlib.md5(fd.read()).hexdigest()

    return hsum


def print_screen(screen_bytes, dest=None):
    """convert screendump data into ascii or .pbm for format

    Parameters
    ----------
        screen_bytes: numpy array
        dest : str
            filename (optional)

    Returns
    -------
        None
            prints screen data as ascii
            If dest filename is given screen data is writen as pbm image

    """

    dat = _dump_screen(screen_bytes)

    if dest is None:     # maybe also .txt files ?
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

    elif dest.endswith('.pbm'):    # Black & White bitmap in simple Netpbm format
        with open(dest, "w", encoding="utf-8") as fd:
            print(f"P1\n{SCREEN_H + 1} {SCREEN_W}", file=fd)
            for y in range(0, SCREEN_W):
                print(numpy.array2string(dat[:, y], max_line_width=300)[1:-1], file=fd)
    elif dest.endswith('.ppm'):    # Orange and Black color RGB image stored in PPM format
        with open(dest, "w", encoding="utf-8") as fd:
            print(f"P3\n{SCREEN_H + 1} {SCREEN_W}\n255", file=fd)
            for y in range(0, SCREEN_W):
                print(" ".join(['255 165 000' if c == '1' else '000 000 000' for c in dat[:, y]]))

    else:
        raise cmdException("invalid filename")


def _dump_screen(screen_bytes):
    """process` screendump data

    Parameters
    ----------
        bytes: screen_bytes

    Returns
    -------
        numpy array

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


def flipper_tree_walk(dpath, proto):
    """Directory tree generator for flipper

    Parameters
    ----------
        dpath: str
            path to top of directory tree to follow
        proto : FlipperProto obj

    Returns
    -------
        yields a tuple containing:
            dirpath: str
                path to current directory in tree
            dirnamess: list
                list of subdirectories in dirpath
            filenames: list
                list of filenames in dirpath

    """
    list_resp = proto.cmd_storage_list(dpath)
    dlist = []
    flist = []

    for li in list_resp:
        if li['type'] == "DIR":
            dlist.append(li['name'])
        else:
            flist.append(li['name'])

    # print(dlist)
    yield dpath, dlist, flist
    for d in dlist:
        yield from flipper_tree_walk(dpath + '/' + d, proto)


def datetime2dict(dt=None):
    """Convert datetime obj into type dict

    Parameters
    ----------
        dt : datetime obj

    Returns
    -------
        dict type containing 'year' 'month' 'day' 'hour' 'minute' 'second' 'weekday'


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
    """Convert type dict into datetime obj

    Parameters
    ----------
    d : dicy
        dict type containing 'year' 'month' 'day' 'hour' 'minute' 'second' 'weekday'

    Returns
    -------
        datetime obj

    Raises
    ----------
        TypeError

    """

    tdict = d.copy()    # we dont want to destroy the caller's data
    del tdict['weekday']
    return datetime.datetime(**tdict)
