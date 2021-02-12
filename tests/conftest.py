import json
from pathlib import Path
from typing import Tuple

import pytest

subs = {
    "Helo": "Hello",
    "helo": "hello",
}


content = """
Helo world !
just came here to say helo.
"""

expected = """
Hello world !
just came here to say hello.
"""


@pytest.fixture(scope="function")
def simple_setup(tmp_path) -> Tuple[Path, Path, str]:
    target = tmp_path / "hello.txt"
    target.write_text(content)
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump(subs, fh)

    return target, subs_file, expected
