# learn-python

[![CI][ci-badge]][ci-url]
[![CD][cd-badge]][cd-url]
[![PyPI version][pypi-badge]][pypi-url]
[![readthedocs build status][docs-badge]][docs-url]
[![License: Apache][apache-badge]][apache-url]
[![pre-commit][pre-commit-badge]][pre-commit-url]
[![Github pages][gh-pages-badge]][gh-pages-url]

[ci-url]: https://github.com/kagemeka/learn-python/actions/workflows/package-ci.yaml
[ci-badge]: https://github.com/kagemeka/learn-python/actions/workflows/package-ci.yaml/badge.svg
[cd-url]: https://github.com/kagemeka/learn-python/actions/workflows/package-cd.yaml
[cd-badge]: https://github.com/kagemeka/learn-python/actions/workflows/package-cd.yaml/badge.svg
[docs-badge]: https://readthedocs.org/projects/lpk/badge/?version=latest
[docs-url]: https://lpk.readthedocs.io
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[apache-badge]: https://img.shields.io/badge/License-Apache2.0-brightgreen.svg
[apache-url]: https://opensource.org/licenses/Apache-2.0
[pypi-badge]: https://badge.fury.io/py/lpk.svg
[pypi-url]: https://badge.fury.io/py/lpk
[gh-pages-badge]: https://github.com/kagemeka/learn-python/actions/workflows/pages/pages-build-deployment/badge.svg
[gh-pages-url]: https://kagemeka.github.io/learn-python

## module

minimum unit of module is a python file. \
a directory containing python files is also a module. \
a single file module is a binary `__main__` when executed as `python3 <path/to/file>.py`, also is a library `__init__` when imported. \
a directory module can be a binary and executed as `python3 <path/to/directory>` by containing`__main__.py`, also can be a library and imported by containing`__init__.py`. \
python to `module/__init__.py` is as rust to `module/mod.rs`.
python to `module.py` is almost as rust to `module.rs` but also a binary.
top level `module/__main__.py` or `module.py` is as rust to `src/main.rs`
top level `module/__init__.py` or `module.py` is as rust to `src/lib.rs`

`__main__` and `__init__` are parts of meta info of a module.
there are a lot of other meta info. e.g. `__name__`

## package

package is also a module or collection of modules.
a package can be published to <https://pypi.org/>.
in actual, body of a package uploaded to the pypi registry is just a single module or some modules.
modules of a package are located under the project directly or the src directory by convention.

## poetry

<https://python-poetry.org/docs/>

the best package managing tool in Python project.
it was insipired by Rust's Cargo.

### manifest file

`pyproject.toml`
<https://python-poetry.org/docs/pyproject/>

### initialize a package

```sh
poetry init # current directory
poetry new <another> # create another package under current directory
```

### check virtual environments

```sh
poetry env info # check executable section and set this custom path when using vscode via `Python: select interpreter`.
poetry env list
```

### clear cache

```sh
poetry cache clear pypi --all
find . | grep -E "__pycache__$" | xargs rm -rf
```

### publish package

- <https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-using-poetry-aa804533fc6f>
- <https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04>

make sure there is not same name package on <https://pypi.org>

```sh
poetry search <package>
```

currently you cannot publish with username and password.
you need to use api token.

```sh
poetry build
poetry publish -u=__token__ -p=<your pypi api token>
```

if it's redundant to input token every time.

```sh
poetry config pypi-token.pypi <your pypi api token>
```

and after that

```sh
poetry build
poetry publish
```

## process sources in a file only when executed as binary

```py
# processed whenever regardless of as library or binary.
...


if __name__ == __main__:
    # processed only when executed as binary.
    ...
```

## testing

by convention, integration tests are located under top level tests directory.
and unittests are included in each module.

- frameworks
  - unittest
    - (std lib)
    - <https://docs.python.org/3/library/unittest.html>
  - doctest
    - (std lib)
    - <https://docs.python.org/3/library/doctest.html>
  - pytest
    - <https://docs.pytest.org/>
    - <https://github.com/pytest-dev/pytest>
    - <https://pypi.org/project/pytest/>

## documenting

- standard or third-party tools list summary
  - <https://realpython.com/documenting-python-code/#documentation-tools-and-resources>
  - <https://wiki.python.org/moin/DocumentationTools>

- hosting
  - readthedocs
    - <https://readthedocs.org/>
    - <https://docs.readthedocs.io/en/stable/>
  - github pages
  - custom domain site of yours.
- generating/building
  - sphinx
    - <https://www.sphinx-doc.org/en/master/>
    - <https://github.com/sphinx-doc/sphinx>
    - <https://pypi.org/project/Sphinx/>
    - functionality
      - autodoc rst from codes
      - build static htmls from rst
    - publish
      - usually automatically build & hosted from rst with readthedocs in CI/CD.
      - you can also build html locally or in CI/CD & host on your own website.

    ```sh
    # first, create conf.py and index.rst in <docs_source_path> like this package.
    # then
    ./sphinx_build.sh
    # open generated <docs_path>/sphinx_build/index.html
    ```

  - mkdocs
    - <https://www.mkdocs.org/>
    - <https://pypi.org/project/mkdocs/>
    - <https://github.com/mkdocs/mkdocs>
    - functionality
      - build static static htmls from markdowns
      - cannot autodoc from codes.
  - pdoc (easy, simple)
    - <https://pypi.org/project/pdoc/>
    - <https://github.com/mitmproxy/pdoc>
    - <https://pdoc.dev/>
    - functionality
      - autodoc & build static htmls from codes
    - publish
      - you can also build html locally or in CI/CD pipelines, then host on your own website, github pages or other hosting services ...
      - automate this processes with CI/CD like github actions.

    ```sh
    ./pdoc_build.sh
    # open generated docs/with_pdoc/index.html
    ```

## linting

- <https://code.visualstudio.com/docs/python/linting>
- <https://code.visualstudio.com/docs/python/linting#_specific-linters>
- linter
  - pylint
    - <https://github.com/PyCQA/pylint>
    - <https://www.pylint.org/>
    - <https://docs.pylint.org/>
    - <https://pypi.org/project/pylint/>
  - flake8 (we recommend this)
    - <https://flake8.pycqa.org/en/latest/>
    - <https://pypi.org/project/flake8/>
    - <https://github.com/PyCQA/flake8>
  - mypy (we recommend)
    - (typing linter)
    - <https://mypy-lang.org/>
    - <https://mypy.readthedocs.io/en/stable/>
    - <https://github.com/python/mypy>
    - <https://pypi.org/project/mypy/>
  - pycodestyle
    - (pep8 based)
    - <https://pypi.org/project/pycodestyle/>
    - <https://pycodestyle.pycqa.org/en/latest/>
    - <https://github.com/PyCQA/pycodestyle>
  - pydocstyle
    - <http://www.pydocstyle.org/en/stable/>
    - <https://pypi.org/project/pydocstyle/>
    - <https://github.com/PyCQA/pydocstyle>
  - prospector
    - <https://prospector.landscape.io/en/master/>
    - <https://pypi.org/project/prospector/>
    - <https://github.com/PyCQA/prospector>
  - pylama
    - <https://klen.github.io/pylama/>
    - <https://github.com/klen/pylama>
    - <https://pypi.org/project/pylama/>
  - bandit
    - <https://bandit.readthedocs.io/en/latest/>
    - <https://github.com/PyCQA/bandit>
    - <https://pypi.org/project/bandit/>

## formatting

- formatter
  - black (we recommend)
    - <https://github.com/psf/black>
    - <https://black.readthedocs.io/en/stable/>
    - <https://pypi.org/project/black/>
  - autopep8
    - <https://pypi.org/project/autopep8/>
    - <https://github.com/peter-evans/autopep8>
  - isort (we recommend)
    - sort imports
    - <https://github.com/PyCQA/isort>
    - <https://pycqa.github.io/isort/>
    - <https://pypi.org/project/isort/>

## CI/CD & automation supporting

- frameworks
  - tox
    - <https://tox.wiki/en/latest/index.html>
    - <https://pypi.org/project/tox/>
    - <https://github.com/tox-dev/tox>
  - nox
    - <https://nox.thea.codes/en/stable/>
    - <https://github.com/wntrblm/nox>
    - <https://pypi.org/project/nox/>
  - invoke
    - <https://www.pyinvoke.org/>
    - <https://github.com/pyinvoke/invoke/>
    - <https://pypi.org/project/invoke/>

## Python public / private syntax convention

there is no private module and file private objects limited by syntax.
by convention, to convey that a module or object is private to users,
you can make it start with a single underscore `_`.
and objects private too.
on the other hand, class members can be public, protected, private
protected member start with a single underscore `_`.
private member start with two under scores `__`.
class to protected member is as a file to private object.
private member is completely different. cannot accessible from outside normally. to access it, `obj._ClassName__private_member`
also, private members are not inherited, so cannot be accessible anyhow through the childeren which inherited it.

## development with vscode

### extensions

- Python
- Pylance
- Live Server
- Even Better TOML
- Bash IDE
- autoDocstring - Python
- GitLens
- markdownlint
- YAML
- shell-format
