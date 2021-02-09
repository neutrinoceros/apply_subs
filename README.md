# `apply-subs`
[![codecov](https://codecov.io/gh/neutrinoceros/apply_subs/branch/main/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/apply_subs)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/apply_subs/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/apply_subs/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`data.json`
```json
{
    "helo": "Hello",
}
```

Then from a shell
```shell
apply-subs hello.txt data.json
```

```patch
...
```
