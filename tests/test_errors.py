import json

from apply_subs.main import main


def test_missing_target(simple_setup, capsys):
    target, subs_file, expected = simple_setup

    typo_target = target.with_suffix(".this_file_doesnt_exists")
    assert not typo_target.exists()

    retval = main([str(typo_target), str(subs_file)])
    assert retval != 0

    out, err = capsys.readouterr()
    assert out == ""
    assert err == f"Error: {typo_target} not found.\n"


def test_invalid_schema(tmp_path, capsys):
    target = tmp_path / "hello.txt"
    target.write_text("nothing")
    subs_file = tmp_path / "subs.json"
    with open(subs_file, "w") as fh:
        json.dump({"A": 0.78}, fh)

    ret = main([str(target), str(subs_file)])
    out, err = capsys.readouterr()
    assert ret != 0
    assert out == ""
    assert err == "Error: unrecognized json schema.\n"
