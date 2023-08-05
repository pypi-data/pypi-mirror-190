# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'binary_module': 'src/binary_module',
 'learn_python': 'src/learn_python',
 'learn_python.second': 'src/learn_python/second',
 'learn_python.second.third': 'src/learn_python/second/third',
 'library_module': 'src/library_module',
 'library_module._private_dir_module': 'src/library_module/_private_dir_module',
 'library_module.chains': 'src/library_module/chains',
 'library_module.just_dir': 'src/library_module/just_dir',
 'library_module.public_dir_module': 'src/library_module/public_dir_module'}

packages = \
['another_module',
 'binary_module',
 'learn_python',
 'learn_python.second',
 'learn_python.second.third',
 'library_module',
 'library_module._private_dir_module',
 'library_module.chains',
 'library_module.just_dir',
 'library_module.public_dir_module']

package_data = \
{'': ['*']}

modules = \
['single_file_module']
extras_require = \
{'nb': ['numba>=0.56.4,<0.57.0'],
 'np': ['scipy>=1.10,<1.11'],
 'np:python_version < "3.11"': ['numpy>=1.23,<2.0', 'numpy>=1.23,<2.0'],
 'np:python_version >= "3.11"': ['numpy>=1,<2', 'numpy>=1,<2']}

entry_points = \
{'console_scripts': ['binary-module-cli = binary_module:main',
                     'lib-hello = library_module.public:public_hello']}

setup_kwargs = {
    'name': 'lpk',
    'version': '0.1.5',
    'description': 'learning python',
    'long_description': '# learn-python\n\n[![CI][ci-badge]][ci-url]\n[![CD][cd-badge]][cd-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![readthedocs build status][docs-badge]][docs-url]\n[![License: Apache][apache-badge]][apache-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-url]: https://github.com/kagemeka/learn-python/actions/workflows/package-ci.yaml\n[ci-badge]: https://github.com/kagemeka/learn-python/actions/workflows/package-ci.yaml/badge.svg\n[cd-url]: https://github.com/kagemeka/learn-python/actions/workflows/package-cd.yaml\n[cd-badge]: https://github.com/kagemeka/learn-python/actions/workflows/package-cd.yaml/badge.svg\n[docs-badge]: https://readthedocs.org/projects/lpk/badge/?version=latest\n[docs-url]: https://lpk.readthedocs.io\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[apache-badge]: https://img.shields.io/badge/License-Apache2.0-brightgreen.svg\n[apache-url]: https://opensource.org/licenses/Apache-2.0\n[pypi-badge]: https://badge.fury.io/py/lpk.svg\n[pypi-url]: https://badge.fury.io/py/lpk\n[gh-pages-badge]: https://github.com/kagemeka/learn-python/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/learn-python\n\n## module\n\nminimum unit of module is a python file. \\\na directory containing python files is also a module. \\\na single file module is a binary `__main__` when executed as `python3 <path/to/file>.py`, also is a library `__init__` when imported. \\\na directory module can be a binary and executed as `python3 <path/to/directory>` by containing`__main__.py`, also can be a library and imported by containing`__init__.py`. \\\npython to `module/__init__.py` is as rust to `module/mod.rs`.\npython to `module.py` is almost as rust to `module.rs` but also a binary.\ntop level `module/__main__.py` or `module.py` is as rust to `src/main.rs`\ntop level `module/__init__.py` or `module.py` is as rust to `src/lib.rs`\n\n`__main__` and `__init__` are parts of meta info of a module.\nthere are a lot of other meta info. e.g. `__name__`\n\n## package\n\npackage is also a module or collection of modules.\na package can be published to <https://pypi.org/>.\nin actual, body of a package uploaded to the pypi registry is just a single module or some modules.\nmodules of a package are located under the project directly or the src directory by convention.\n\n## poetry\n\n<https://python-poetry.org/docs/>\n\nthe best package managing tool in Python project.\nit was insipired by Rust\'s Cargo.\n\n### manifest file\n\n`pyproject.toml`\n<https://python-poetry.org/docs/pyproject/>\n\n### initialize a package\n\n```sh\npoetry init # current directory\npoetry new <another> # create another package under current directory\n```\n\n### check virtual environments\n\n```sh\npoetry env info # check executable section and set this custom path when using vscode via `Python: select interpreter`.\npoetry env list\n```\n\n### clear cache\n\n```sh\npoetry cache clear pypi --all\nfind . | grep -E "__pycache__$" | xargs rm -rf\n```\n\n### publish package\n\n- <https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-using-poetry-aa804533fc6f>\n- <https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04>\n\nmake sure there is not same name package on <https://pypi.org>\n\n```sh\npoetry search <package>\n```\n\ncurrently you cannot publish with username and password.\nyou need to use api token.\n\n```sh\npoetry build\npoetry publish -u=__token__ -p=<your pypi api token>\n```\n\nif it\'s redundant to input token every time.\n\n```sh\npoetry config pypi-token.pypi <your pypi api token>\n```\n\nand after that\n\n```sh\npoetry build\npoetry publish\n```\n\n## process sources in a file only when executed as binary\n\n```py\n# processed whenever regardless of as library or binary.\n...\n\n\nif __name__ == __main__:\n    # processed only when executed as binary.\n    ...\n```\n\n## testing\n\nby convention, integration tests are located under top level tests directory.\nand unittests are included in each module.\n\n- frameworks\n  - unittest\n    - (std lib)\n    - <https://docs.python.org/3/library/unittest.html>\n  - doctest\n    - (std lib)\n    - <https://docs.python.org/3/library/doctest.html>\n  - pytest\n    - <https://docs.pytest.org/>\n    - <https://github.com/pytest-dev/pytest>\n    - <https://pypi.org/project/pytest/>\n\n## documenting\n\n- standard or third-party tools list summary\n  - <https://realpython.com/documenting-python-code/#documentation-tools-and-resources>\n  - <https://wiki.python.org/moin/DocumentationTools>\n\n- hosting\n  - readthedocs\n    - <https://readthedocs.org/>\n    - <https://docs.readthedocs.io/en/stable/>\n  - github pages\n  - custom domain site of yours.\n- generating/building\n  - sphinx\n    - <https://www.sphinx-doc.org/en/master/>\n    - <https://github.com/sphinx-doc/sphinx>\n    - <https://pypi.org/project/Sphinx/>\n    - functionality\n      - autodoc rst from codes\n      - build static htmls from rst\n    - publish\n      - usually automatically build & hosted from rst with readthedocs in CI/CD.\n      - you can also build html locally or in CI/CD & host on your own website.\n\n    ```sh\n    # first, create conf.py and index.rst in <docs_source_path> like this package.\n    # then\n    ./sphinx_build.sh\n    # open generated <docs_path>/sphinx_build/index.html\n    ```\n\n  - mkdocs\n    - <https://www.mkdocs.org/>\n    - <https://pypi.org/project/mkdocs/>\n    - <https://github.com/mkdocs/mkdocs>\n    - functionality\n      - build static static htmls from markdowns\n      - cannot autodoc from codes.\n  - pdoc (easy, simple)\n    - <https://pypi.org/project/pdoc/>\n    - <https://github.com/mitmproxy/pdoc>\n    - <https://pdoc.dev/>\n    - functionality\n      - autodoc & build static htmls from codes\n    - publish\n      - you can also build html locally or in CI/CD pipelines, then host on your own website, github pages or other hosting services ...\n      - automate this processes with CI/CD like github actions.\n\n    ```sh\n    ./pdoc_build.sh\n    # open generated docs/with_pdoc/index.html\n    ```\n\n## linting\n\n- <https://code.visualstudio.com/docs/python/linting>\n- <https://code.visualstudio.com/docs/python/linting#_specific-linters>\n- linter\n  - pylint\n    - <https://github.com/PyCQA/pylint>\n    - <https://www.pylint.org/>\n    - <https://docs.pylint.org/>\n    - <https://pypi.org/project/pylint/>\n  - flake8 (we recommend this)\n    - <https://flake8.pycqa.org/en/latest/>\n    - <https://pypi.org/project/flake8/>\n    - <https://github.com/PyCQA/flake8>\n  - mypy (we recommend)\n    - (typing linter)\n    - <https://mypy-lang.org/>\n    - <https://mypy.readthedocs.io/en/stable/>\n    - <https://github.com/python/mypy>\n    - <https://pypi.org/project/mypy/>\n  - pycodestyle\n    - (pep8 based)\n    - <https://pypi.org/project/pycodestyle/>\n    - <https://pycodestyle.pycqa.org/en/latest/>\n    - <https://github.com/PyCQA/pycodestyle>\n  - pydocstyle\n    - <http://www.pydocstyle.org/en/stable/>\n    - <https://pypi.org/project/pydocstyle/>\n    - <https://github.com/PyCQA/pydocstyle>\n  - prospector\n    - <https://prospector.landscape.io/en/master/>\n    - <https://pypi.org/project/prospector/>\n    - <https://github.com/PyCQA/prospector>\n  - pylama\n    - <https://klen.github.io/pylama/>\n    - <https://github.com/klen/pylama>\n    - <https://pypi.org/project/pylama/>\n  - bandit\n    - <https://bandit.readthedocs.io/en/latest/>\n    - <https://github.com/PyCQA/bandit>\n    - <https://pypi.org/project/bandit/>\n\n## formatting\n\n- formatter\n  - black (we recommend)\n    - <https://github.com/psf/black>\n    - <https://black.readthedocs.io/en/stable/>\n    - <https://pypi.org/project/black/>\n  - autopep8\n    - <https://pypi.org/project/autopep8/>\n    - <https://github.com/peter-evans/autopep8>\n  - isort (we recommend)\n    - sort imports\n    - <https://github.com/PyCQA/isort>\n    - <https://pycqa.github.io/isort/>\n    - <https://pypi.org/project/isort/>\n\n## CI/CD & automation supporting\n\n- frameworks\n  - tox\n    - <https://tox.wiki/en/latest/index.html>\n    - <https://pypi.org/project/tox/>\n    - <https://github.com/tox-dev/tox>\n  - nox\n    - <https://nox.thea.codes/en/stable/>\n    - <https://github.com/wntrblm/nox>\n    - <https://pypi.org/project/nox/>\n  - invoke\n    - <https://www.pyinvoke.org/>\n    - <https://github.com/pyinvoke/invoke/>\n    - <https://pypi.org/project/invoke/>\n\n## Python public / private syntax convention\n\nthere is no private module and file private objects limited by syntax.\nby convention, to convey that a module or object is private to users,\nyou can make it start with a single underscore `_`.\nand objects private too.\non the other hand, class members can be public, protected, private\nprotected member start with a single underscore `_`.\nprivate member start with two under scores `__`.\nclass to protected member is as a file to private object.\nprivate member is completely different. cannot accessible from outside normally. to access it, `obj._ClassName__private_member`\nalso, private members are not inherited, so cannot be accessible anyhow through the childeren which inherited it.\n\n## development with vscode\n\n### extensions\n\n- Python\n- Pylance\n- Live Server\n- Even Better TOML\n- Bash IDE\n- autoDocstring - Python\n- GitLens\n- markdownlint\n- YAML\n- shell-format\n',
    'author': 'kagemeka',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'kagemeka',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/learn-python/README.md',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
