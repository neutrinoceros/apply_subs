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


def test_missing_target(simple_setup, capsys):
    target, subs_file, expected = simple_setup

    typo_target = target.with_suffix(".this_file_doesnt_exists")
    assert not typo_target.exists()

    retval = main([str(typo_target), str(subs_file)])
    assert retval != 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err == f"Error: {typo_target} not found.\n"


def test_broken_call(simple_setup, capsys, monkeypatch):
    target, subs_file, expected = simple_setup

    monkeypatch.setattr("apply_subs.main.BASE_COMMAND", ["not_a_real_command $HOME"])

    retval = main([str(target), str(subs_file)])
    assert retval != 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err == f"Error: failed to apply subsitutions to {target}\n"
