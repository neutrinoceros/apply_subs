import configparser
from pathlib import Path

import pytest

from apply_subs import __version__
from apply_subs.main import main

USAGE_MESSAGE = """usage: apply-subs [-h] [-s SUBS] [-i | -d | -cp] [-v] [target ...]

positional arguments:
  target                target text file(s)

optional arguments:
  -h, --help            show this help message and exit
  -s SUBS, --subs SUBS  json file describing substitutions to apply (order
                        matters).
  -i, --inplace
  -d, --diff            print a diff.
  -cp, --cdiff, --colored-diff
                        print a colored diff.
  -v, --version         print apply-subs version.
"""


@pytest.mark.parametrize("argv", (["apply-subs"], ["apply-subs", "file1"]))
def test_missing_positionals(argv, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", argv)
    ret = main()
    out, err = capsys.readouterr()

    assert ret != 0
    assert out == ""
    # skip the first line because it differs between macos and linux
    assert err.splitlines()[1:] == USAGE_MESSAGE.splitlines()[1:]


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
