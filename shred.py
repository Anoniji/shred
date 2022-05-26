#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse


def sdell(path, passes, rand, buffer):
    if os.path.isdir(path):
        print(' - SCAN  :', path)
        for data in os.walk(path):
            if len(data[-1]) > 0:
                for file in data[-1]:
                    f_path = os.path.join(data[0], file)
                    sdell(f_path, passes, rand, buffer)

    elif os.path.isfile(path):
        print(' - REMOVE:', path)
        length = os.path.getsize(path)
        with open(path, "br+", buffering=buffer) as f:
            for i in range(passes):
                f.seek(0)
                if rand:
                    r = os.urandom(length)
                    sys.stdout.write(str(r) + '     \r')
                    sys.stdout.flush()
                    f.write(r)
                else:
                    f.write(b'\x00')
            f.close()

        print('\n - REMOVE FILE')
        os.remove(path)

    else:
        raise ValueError('No data to delete')


# Main PY
if __name__ == '__main__':
    # Clear cmd
    os.system('cls' if os.name == 'nt' else 'clear')

    # ARG
    p = argparse.ArgumentParser()
    p.add_argument(
        '-d',
        '--path',
        type=str,
        required=True
    )
    p.add_argument(
        '-n',
        '--passes',
        type=int,
        default=1,
    )
    p.add_argument(
        '-z',
        '--rand',
        action='store_true',
    )
    p.add_argument(
        '-b',
        '--buffer',
        type=int,
        default=-1,
    )
    p.add_argument(
        '-v',
        '--verbose',
        action='store_true',
    )
    a = p.parse_args()
    a_path, a_passes, a_rand, a_buffer, a_verbose = (
        a.path, a.rand, a.passes, a.buffer, a.verbose
    )

    if not a_verbose:
        sys.stdout = open(os.devnull, 'w')

    try:
        sdell(a_path, a_passes, a_rand, a_buffer)
    except Exception as e:
        sys.stdout = sys.__stdout__
        print('error', e)

    if not a_verbose:
        sys.stdout = sys.__stdout__
