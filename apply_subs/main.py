#!/usr/bin/env python3

import argparse
import json
import sys
import tempfile
from shutil import copy
from subprocess import SubprocessError, run


def _sub(old: str, new: str, filename: str) -> str:
    comm = ["sed", "-i", "-e", f"s/{old}/{new}/g", filename]
    res = run(comm, capture_output=True, check=True)
    return res.stdout.decode()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="")
    parser.add_argument(
        "subs", help="json file describing substitutions to apply (order matters)."
    )
    parser.add_argument("-i", "--inplace", action="store_true")
    args = parser.parse_args(argv)

    with open(args.subs, "r") as fh:
        subs = json.load(fh)

    with tempfile.NamedTemporaryFile() as workfile:
        copy(args.target, workfile.name)
        for old, new in subs.items():
            try:
                _sub(old, new, workfile.name)
            except SubprocessError:
                print(
                    f"Error in applying subsitutions to {args.target}", file=sys.stderr
                )
                return 1
        with open(workfile.name, "r") as fh:
            new_content = fh.read()
    if args.inplace:
        with open(args.target, "w") as fh:
            fh.write(new_content)
    else:
        print(new_content, end="")
    return 0
