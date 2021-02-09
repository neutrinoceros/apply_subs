import json

import pytest

from apply_subs.main import main

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


def test_main(tmp_path, capsys):
    target = tmp_path / "hello.txt"
    target.write_text(content)
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump(subs, fh)

    retval = main([str(target), str(subs_file)])
    assert retval == 0

    out, err = capsys.readouterr()
    assert out == expected
    assert err == ""


@pytest.mark.parametrize("flag", ["-i", "--inplace"])
def test_inplace_substitution(tmp_path, capsys, flag: str):
    target = tmp_path / "hello.txt"
    target.write_text(content)
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump(subs, fh)

    retval = main([str(target), str(subs_file), flag])
    assert retval == 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""

    actual = target.read_text()
    assert actual == expected
