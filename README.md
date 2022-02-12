# Python Logfmter

[![pre-commit](https://github.com/jteppinette/python-logfmter/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/jteppinette/python-logfmter/actions/workflows/pre-commit.yml)
[![test](https://github.com/jteppinette/python-logfmter/actions/workflows/test.yml/badge.svg)](https://github.com/jteppinette/python-logfmter/actions/workflows/test.yml)

_A Python package which supports global [logfmt](https://www.brandur.org/logfmt) formatted logging._

## Install

```sh
$ pip install logfmter
```

## Usage

Before integrating this library, you should be familiar with Python's logging
functionality. I recommend reading the [Basic Logging
Tutorial](https://docs.python.org/3/howto/logging.html).

This package exposes a single `Logfmter` class that can be integrated into
the standard library logging system similar to any `logging.Formatter`.

The provided formatter will logfmt encode all logs. Key value pairs are provided
via the `extra` keyword argument or by passing a dictionary as the log message.

**Basic**

```python
import logging
from logfmter import Logfmter

handler = logging.StreamHandler()
handler.setFormatter(Logfmter())

logging.basicConfig(handlers=[handler])

logger.error("hello", extra={"alpha": 1}) # at=ERROR msg=hello alpha=1
logger.error({"token": "Hello, World!"}) # at=ERROR token="Hello, World!"
```

**Customize**

You can subclass the formatter to change its behavior.

```python
import logging
from logfmter import Logfmter


class CustomLogfmter(Logfmter):
    """
    Provide a custom logfmt formatter which formats
    booleans as "yes" or "no" strings.
    """

    @classmethod
    def format_value(cls, value):
        if isinstance(value, bool):
            return "yes" if value else "no"

	return super().format_value(value)

handler = logging.StreamHandler()
handler.setFormatter(CustomLogfmter())

logging.basicConfig(handlers=[handler])

logger.error({"example": True}) # at=ERROR example=yes
```

## Development

### Required Software

Refer to the links provided below to install these development dependencies:

- [direnv](https://direnv.net)
- [git](https://git-scm.com/)
- [pyenv](https://github.com/pyenv/pyenv#installation)

### Getting Started

**Setup**

```sh
$ <runtimes.txt xargs -n 1 pyenv install -s
$ direnv allow
$ pip install -r requirements/dev.txt
$ pre-commit install
$ pip install -e .
```

**Tests**

_Run the test suite against the active python environment._

```sh
$ pytest
```

_Run the test suite against the active python environment and
watch the codebase for any changes._

```sh
$ ptw
```

_Run the test suite against all supported python versions._

```sh
$ tox
```

### Publishing

**Create**

1. Update the version number in `logfmter/__init__.py`.

2. Add an entry in `HISTORY.md`.

3. Commit the changes, tag the commit, and push the tags:

   ```sh
   $ git commit -am "v<major>.<minor>.<patch>"
   $ git tag v<major>.<minor>.<patch>
   $ git push --tags
   ```

4. Convert the tag to a release in GitHub with the history
   entry as the description.

**Build**

```sh
$ python -m build
```

**Upload**

```
$ twine upload dist/*
```
