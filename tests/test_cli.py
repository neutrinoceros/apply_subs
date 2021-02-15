import configparser
from pathlib import Path

import pytest

from apply_subs import __version__
from apply_subs.main import main

HELP_MESSAGE = """
usage: apply-subs [-h] [-s SUBS] [-i | -d | -cp] [-v] [target ...]

positional arguments:
  target                target text file(s)

optional arguments:
  -h, --help            show this help message and exit
  -s SUBS, --subs SUBS  json file describing substitutions to apply (order
                        matters).
  -i, --inplace
  -d, --diff            print a diff.
  -cd, --cd, --cdiff, --colored-diff
                        print a colored diff.
  -v, --version         print apply-subs version.
"""


@pytest.mark.parametrize(
    "argv,expected_err",
    (
        (["apply-subs"], "Error: no target file provided."),
        (["apply-subs", "file1"], "Error: `--subs/-s` flag is mandatory."),
    ),
)
def test_missing_positionals(argv, expected_err, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", argv)
    ret = main()
    out, err = capsys.readouterr()

    assert ret != 0
    assert out == ""
    assert err.splitlines()[0] == expected_err
    # skip the first line because it differs between macos and linux
    assert err.splitlines()[2:] == HELP_MESSAGE.splitlines()[2:]


def test_broken_json(capsys, tmp_path):
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.json"
    f1.touch()
    f2.touch()
    ret = main([str(f1), "--subs", str(f2)])
    out, err = capsys.readouterr()

    assert ret != 0
    assert out == ""
    assert err.replace("\n", "") == f"Error: invalid json file `{f2}`"


@pytest.mark.parametrize("flag", ["-v", "--version"])
def test_version(flag, capsys):
    ret = main([flag])
    out, err = capsys.readouterr()
    assert ret == 0
    assert out == f"{__version__}\n"
    assert err == ""


def test_config_version():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parents[1] / "setup.cfg")
    expected = __version__
    actual = config["metadata"]["version"]
    assert actual == expected


def test_empty_diff(tmp_path, capsys):
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.json"
    f1.touch()
    f2.write_text('{"nothing": "emtpy"}')
    ret = main([str(f1), "--subs", str(f2), "--diff"])
    out, err = capsys.readouterr()

    assert ret == 0
    assert out == ""
    assert err == ""
