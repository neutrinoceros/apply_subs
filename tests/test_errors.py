import json

from apply_subs.main import main


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
