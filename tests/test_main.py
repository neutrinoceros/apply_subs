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


@pytest.mark.parametrize(
    "flag", ["-p", "--patch", "-cp", "--cpatch", "--colored-patch"]
)
def test_patch(simple_setup, capsys, monkeypatch, flag: str):
    target, subs_file, _expected = simple_setup

    class ColorFallBack:
        def __getattr__(self, name):
            return ""

    monkeypatch.setattr("apply_subs.main.Fore", ColorFallBack())

    retval = main([str(target), str(subs_file), flag])
    assert retval == 0

    expected = (
        "-Helo world !\n"
        "-just came here to say helo.\n"
        "+Hello world !\n"
        "+just came here to say hello.\n\n"
    )
    out, err = capsys.readouterr()
    res = "".join(out.splitlines(keepends=True)[4:])
    assert res == expected
    assert err == ""
