# `apply-subs`
[![codecov](https://codecov.io/gh/neutrinoceros/apply_subs/branch/main/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/apply_subs)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/apply_subs/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/apply_subs/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Apply a dictionnary (json) of substitutions to a text file.
## Installing

From the top level of the repo
```shell
$ pip install .
```

## Example

`mytext.txt`
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```

`mysubs.json` contains the substitutions (new: old)
```json
{
    "Hello": "Lorem ipsum",
     "goodbye": "magna aliqua",
}
```

Then from a shell
```shell
$ apply-subs mytext.txt mysubs.json
```

Will print
```
Hello dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore goodbye.
```

Inplace substitutions (`-i/--inplace`)
```
apply-subs --inplace mytext.txt mysubs.json
```
which is equivalent to
```
apply-subs mytext.txt mysubs.json > mytext.txt
```

>Patch mode (`-p/--patch`)
>prints a patch diff instead of the end result
>NOT IMPLEMENTED YET
