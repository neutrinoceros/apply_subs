import pytest

from apply_subs.main import main


def test_main(simple_setup, capsys):
    target, subs_file, expected = simple_setup

    retval = main([str(target), str(subs_file)])
    assert retval == 0

    out, err = capsys.readouterr()
    assert out == expected
    assert err == ""


@pytest.mark.parametrize("flag", ["-i", "--inplace"])
def test_inplace_substitution(simple_setup, capsys, flag: str):
    target, subs_file, expected = simple_setup

    retval = main([str(target), str(subs_file), flag])
    assert retval == 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""

    actual = target.read_text()
    assert actual == expected
