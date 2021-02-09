#!/usr/bin/env python3

import argparse
import json
import sys
import tempfile
from pathlib import Path
from shutil import copy
from subprocess import CalledProcessError, run

BASE_COMMAND = ["sed", "-i", "-e"]


def _sub(old: str, new: str, filename: str) -> str:
    comm = BASE_COMMAND + [f"s/{old}/{new}/g", filename]
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

    if not Path(args.target).is_file():
        print(f"Error: {args.target} not found.", file=sys.stderr)
        return 1

    with open(args.subs, "r") as fh:
        subs = json.load(fh)

    with tempfile.NamedTemporaryFile() as workfile:
        copy(args.target, workfile.name)
        for old, new in subs.items():
            try:
                _sub(old, new, workfile.name)
            except (CalledProcessError, FileNotFoundError):
                print(
                    f"Error: failed to apply subsitutions to {args.target}",
                    file=sys.stderr,
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
