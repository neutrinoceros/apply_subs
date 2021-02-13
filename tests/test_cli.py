import configparser
from pathlib import Path

import pytest

from apply_subs import __version__
from apply_subs.main import main

USAGE_MESSAGE = (
    "usage: apply-subs [-h] [-i | -p | -cp] [-v] [target] [subs]\n\n"
    "positional arguments:\n"
    "  target                a target text file.\n"
    "  subs                  json file describing substitutions to apply (order\n"
    "                        matters).\n\n"
    "optional arguments:\n"
    "  -h, --help            show this help message and exit\n"
    "  -i, --inplace\n"
    "  -p, --patch           print a patch.\n"
    "  -cp, --cpatch, --colored-patch\n"
    "                        print a colored patch.\n"
    "  -v, --version         print apply-subs version.\n"
)


@pytest.mark.parametrize("argv", (["apply-subs"], ["apply-subs", "file1"]))
def test_missing_positionals(argv, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", argv)
    ret = main()
    out, err = capsys.readouterr()

    assert ret != 0
    assert out == ""
    assert err == USAGE_MESSAGE


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
