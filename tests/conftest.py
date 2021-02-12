import json
from pathlib import Path
from typing import Tuple

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
