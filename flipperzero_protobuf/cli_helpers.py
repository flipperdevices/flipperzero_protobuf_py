#!/usr/bin/env python3
"""command helper funtions FlipperProto Class"""

import datetime
import hashlib
from collections.abc import Iterator

import numpy

from .flipper_base import InputTypeException

__ALL__ = [
    "print_hex",
    "calc_file_md5",
    "flipper_tree_walk",
    "datetime2dict",
    "dict2datetime",
    "calc_n_print_du",
]


def print_hex(bytes_data) -> None:
    """print bytes in hex"""
    print("".join(f"{x:02x} " for x in bytes_data))


_SCREEN_H = 128
_SCREEN_W = 64


def calc_file_md5(fname) -> str:
    """Calculate md5 hash for file

    Parameters
    ----------
        fname : str
            path to local fole

    Returns
    -------
        str containing md5 message-digest fingerprint for file

    """
    with open(fname, "rb") as fd:
        hsum = hashlib.md5(fd.read()).hexdigest()

    return hsum


def _write_screen(dat) -> None:
    """write image data to terminal screen"""
    for y in range(0, _SCREEN_W, 2):
        for x in range(1, _SCREEN_H + 1):
            if int(dat[x][y]) == 1 and int(dat[x][y + 1]) == 1:
                print("\u2588", end="")
            if int(dat[x][y]) == 0 and int(dat[x][y + 1]) == 1:
                print("\u2584", end="")
            if int(dat[x][y]) == 1 and int(dat[x][y + 1]) == 0:
                print("\u2580", end="")
            if int(dat[x][y]) == 0 and int(dat[x][y + 1]) == 0:
                print(" ", end="")
        print()


def _write_pbm_file(dat, dest) -> None:
    """write Black & White bitmap in simple Netpbm format"""
    with open(dest, "w", encoding="utf-8") as fd:
        print(f"P1\n{_SCREEN_H + 1} {_SCREEN_W}", file=fd)
        for y in range(0, _SCREEN_W):
            print(numpy.array2string(dat[:, y], max_line_width=300)[1:-1], file=fd)


def _write_ppm_file(dat, dest) -> None:
    """write Orange and Black color RGB image stored in PPM format"""
    with open(dest, "w", encoding="utf-8") as fd:
        print(f"P3\n{_SCREEN_H + 1} {_SCREEN_W}\n255", file=fd)
        for y in range(0, _SCREEN_W):
            print(
                " ".join(
                    ["255 165 000" if c == "1" else "000 000 000" for c in dat[:, y]]
                )
            )


def print_screen(screen_bytes, dest=None) -> None:
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

    Raises
    ----------
        InputTypeException

    """

    dat = _dump_screen(screen_bytes)

    if dest is None:  # maybe also .txt files ?
        _write_screen(dat)
        return

    if dest.endswith(".pbm"):  # Black & White bitmap in simple Netpbm format
        _write_pbm_file(dat, dest)
        return

    if dest.endswith(".ppm"):  # Orange and Black color RGB image stored in PPM format
        _write_ppm_file(dat, dest)
        return

    raise InputTypeException("invalid filename: {dest}")


def _dump_screen(screen_bytes) -> numpy.ndarray:
    """process` screendump data

    Parameters
    ----------
        bytes: screen_bytes

    Returns
    -------
        numpy array

    """

    # pylint: disable=multiple-statements

    def get_bin(x) -> str:
        return format(x, "08b")

    scr = numpy.zeros((_SCREEN_H + 1, _SCREEN_W + 1), dtype=int)
    data = screen_bytes

    x = y = 0
    basey = 0

    for i in range(0, int(_SCREEN_H * _SCREEN_W / 8)):
        tmp = get_bin(data[i])[::-1]

        y = basey
        x += 1
        for c in tmp:
            scr[x][y] = c
            y += 1

        if (i + 1) % _SCREEN_H == 0:
            basey += 8
            x = 0

    return scr


def flipper_tree_walk(dpath, proto, filedata=False) -> Iterator[str, list, list]:
    """Directory tree generator for flipper
        writen to have simular call interface as os.walk()

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
    list_resp = proto.rpc_storage_list(dpath)
    dlist = []
    flist = []

    for li in list_resp:
        if li["type"] == "DIR":
            dlist.append(li["name"])
        else:
            if filedata:
                flist.append(li)
            else:
                flist.append(li["name"])

    # print(dlist)
    yield dpath, dlist, flist
    for d in dlist:
        yield from flipper_tree_walk(dpath + "/" + d, proto, filedata=filedata)


def datetime2dict(dt=None) -> dict:
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
        "year": tlist[0],
        "month": tlist[2],
        "day": tlist[3],
        "hour": tlist[4],
        "minute": tlist[5],
        "second": tlist[6],
        "weekday": tlist[7] + 1,
    }

    return datetime_dict


def dict2datetime(d) -> datetime.datetime:
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

    tdict = d.copy()  # we dont want to destroy the caller's data
    del tdict["weekday"]
    return datetime.datetime(**tdict)


def _get_dir_size(flip, dir_path) -> int:
    """calculate disk usage statistics for flipper folder and sub folders."""
    total = 0
    for ROOT, DIRS, FILES in flipper_tree_walk(dir_path, flip, filedata=True):
        for d in DIRS:
            total += _get_dir_size(flip, f"{ROOT}/{d}")
        for f in FILES:
            total += f["size"]

    return total


def calc_n_print_du(flip, dir_path) -> None:
    """prints folder  disk usage statistics."""

    if len(dir_path) > 1:
        dir_path = dir_path.rstrip("/")

    flist = flip.rpc_storage_list(dir_path)

    flist.sort(key=lambda x: (x["type"], x["name"].lower()))

    flist = flip.rpc_storage_list(dir_path)

    total_size = 0
    for line in flist:
        if line["type"] == "DIR":
            dsize = _get_dir_size(flip, f"{dir_path}/{line['name']}")
            total_size += dsize
            n = line["name"] + "/"
            print(f"{n:<25s}\t{dsize:>9d}\tDIR")
            continue

        total_size += line["size"]
        print(f"{line['name']:<25s}\t{line['size']:>9d}")

    print(f"Total: {total_size}")
