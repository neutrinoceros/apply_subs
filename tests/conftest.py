import json
from pathlib import Path
from typing import List, Tuple

import pytest

subs_to_try = [
    {
        # new, old(s)
        "Hello": "Helo",
        "hello": "helo",
    },
    {
        # new, old(s)
        "Hello": ["Helo"],
        "hello": ["helo"],
    },
]


content = """
Helo world !
just came here to say helo.
"""

expected = """
Hello world !
just came here to say hello.
"""


@pytest.fixture(scope="function", params=subs_to_try)
def simple_setup(tmp_path, request) -> Tuple[Path, Path, str]:
    target = tmp_path / "hello.txt"
    target.write_text(content)
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump(request.param, fh)

    return target, subs_file, expected


@pytest.fixture(scope="function", params=subs_to_try)
def multiple_targets_setup(tmp_path, request) -> Tuple[List[Path], Path, str]:
    targets = [tmp_path / f"hello_{n}.txt" for n in range(3)]
    for target in targets:
        target.write_text(content)
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump(request.param, fh)

    return targets, subs_file, expected * 3
