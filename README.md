# apply-subs
![PyPI](https://img.shields.io/pypi/v/apply-subs)
![PyPI](https://img.shields.io/pypi/pyversions/apply_subs?logo=python&logoColor=white&label=Python)
[![codecov](https://codecov.io/gh/neutrinoceros/apply_subs/branch/main/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/apply_subs)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/apply_subs/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/apply_subs/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command line application to apply a dictionnary (json) of substitutions to
text file corpus. This program is a find-and-replace tool to perform a
arbitrarily large set of substitutions in a reproducible fashion.

Disclaimer, this app is far less powerful than `sed` and in particular doesn't
support regex replacement. What it offers a simpler interface to make simple
sweeping changes across a whole project in a reproducible fashion.

# Installation

The easiest installation method is
```shell
$ pip install apply-subs
```
In order to install `apply-subs` in isolation, use [`pipx`](https://pipxproject.github.io/pipx/) instead.


# Examples

`apply-subs` uses a json file as input. This file should specify substitutions
as `new: old`, where `old` can either be a single str, or a list of strings.

## minimal case
```shell
echo "bunnies and bongos and bananas" > mytext.txt
echo '{"bunnies": "rabbits", "SECRETS": ["bongos", "bananas"]}' > mysubs.json
apply-subs mytext.txt -s mysubs.json
```
will print the patched content
```
bunnies and SECRETS and SECRETS
```

## diff mode

Use diff mode (`-d/--diff`) to print a diff instead of the end result
```patch
--- mytext.txt
+++ mytext.txt (patched)
@@ -1 +1 @@
-Lorem ipsum dolor sit amet, consectetur adipiscing elit
+Hello dolor sit amet, consectetur goodbye
```

Use `-cp/--cdiff/--colored-diff` for a colored output (when supported).

## inplace substitutions
`-i/--inplace`
```shell
apply-subs --inplace mytext.txt -s mysubs.json
```
is equivalent to
```shell
apply-subs mytext.txt -s mysubs.json > mytext.txt
```

## target several files in one go

The `target` positional argument can consist of a single file (as illustrated above),
or many. This is useful for instance if you need to apply a set of subtitutions to
all files in a project whose name match a regexp.

```shell
git ls-files | egrep "(.md|.py)$" | xargs apply-subs -s subsubs.json -i
```
