import json
from typing import Tuple

import pytest

from apply_subs.main import main


@pytest.mark.parametrize("missing", [(True, True), (True, False), (False, True)])
def test_missing_files(simple_setup, capsys, missing: Tuple[bool, bool]):
    target, subs_file, _expected = simple_setup

    if missing[0]:
        target = target.with_suffix(".this_file_doesnt_exists")
        assert not target.exists()
        expected_err = f"Error {target} not found."
    if missing[1]:
        subs_file = subs_file.with_suffix(".this_file_doesnt_exists")
        assert not subs_file.exists()
        expected_err = f"Error {subs_file} not found."

    ret = main([str(target), "-s", str(subs_file)])
    assert ret != 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err.replace("\n", "") == expected_err


def test_invalid_schema(tmp_path, capsys):
    target = tmp_path / "hello.txt"
    target.write_text("nothing")
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump({"A": 0.78}, fh)

    ret = main([str(target), "-s", str(subs_file)])
    out, err = capsys.readouterr()
    assert ret != 0
    assert out == ""
    assert err == "Error unrecognized json schema.\n"
