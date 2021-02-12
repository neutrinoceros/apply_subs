#!/usr/bin/env python3

import argparse
import json
import sys
import tempfile
from pathlib import Path
from shutil import copy
from subprocess import CalledProcessError, run
from typing import List, Union

from more_itertools import always_iterable
from schema import Or, Schema

BASE_COMMAND = ["sed", "-i", "-e"]

SUBS_SCHEMA = Schema({str: Or(str, list)})


def _sub(to_replace: Union[str, List[str]], new: str, filename: str) -> str:
    for old in always_iterable(to_replace):
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

    if not SUBS_SCHEMA.is_valid(subs):
        print("Error: unrecognized json schema.", file=sys.stderr)
        return 1

    with tempfile.NamedTemporaryFile() as workfile:
        copy(args.target, workfile.name)
        for new, old in subs.items():
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
