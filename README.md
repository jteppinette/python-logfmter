# Python Logfmter

[![pre-commit](https://github.com/jteppinette/python-logfmter/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/jteppinette/python-logfmter/actions/workflows/pre-commit.yml)
[![test](https://github.com/jteppinette/python-logfmter/actions/workflows/test.yml/badge.svg)](https://github.com/jteppinette/python-logfmter/actions/workflows/test.yml)

_A Python package which supports global [logfmt](https://www.brandur.org/logfmt) formatted logging._

1. [Install](#install)
2. [Usage](#usage)
   1. [Integration](#integration)
   2. [Configuration](#configuration)
   3. [Extend](#extend)
3. [Development](#development)
   1. [Required Software](#required-software)
   2. [Getting Started](#getting-started)
   3. [Publishing](#publishing)

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

If a log message is created via `logging.exception` (inside an exception handler), then
the exception information (traceback, type, and message) will be encoded in the
`exc_info` parameter.

### Integration

**[basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)**

```python
import logging
from logfmter import Logfmter

handler = logging.StreamHandler()
handler.setFormatter(Logfmter())

logging.basicConfig(handlers=[handler])

logging.error("hello", extra={"alpha": 1}) # at=ERROR msg=hello alpha=1
logging.error({"token": "Hello, World!"}) # at=ERROR token="Hello, World!"
```

**[dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)**

```python
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "logfmt": {
                "()": "logfmter.Logfmter",
            }
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "logfmt"}
        },
        "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
    }
)

logging.info("hello", extra={"alpha": 1}) # at=INFO msg=hello alpha=1
```

_Notice, you can configure the `Logfmter` by providing keyword arguments as dictionary
items after `"()"`:_

```python
...

    "logfmt": {
        "()": "logfmter.Logfmter",
        "keys": [...],
        "mapping": {...}
    }

...
```

### Configuration

**keys**

By default, the `at=<levelname>` key/value will be included in all log messages. These
default keys can be overridden using the `keys` parameter. If the key you want to include
in your output is represented by a different attribute on the log record, then you can
use the `mapping` parameter to provide that key/attribute mapping.

Reference the Python [`logging.LogRecord` Documentation](https://docs.python.org/3/library/logging.html?highlight=logrecord#logging.LogRecord)
for a list of available attributes.

```python
import logging
from logfmter import Logfmter

formatter = Logfmter(keys=["at", "processName"])

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(handlers=[handler])

logging.error("hello") # at=ERROR processName=MainProceess msg=hello
```

**mapping**

By default, a mapping of `{"at": "levelname"}` is used to allow the `at` key to reference
the log record's `levelname` attribute. You can override this parameter to provide your
own mappings.

```python
import logging
from logfmter import Logfmter

formatter = Logfmter(
    keys=["at", "process"],
    mapping={"at": "levelname", "process": "processName"}
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(handlers=[handler])

logging.error("hello") # at=ERROR process=MainProceess msg=hello
```

**datefmt**

If you request the `asctime` attribute (directly or through a mapping), then the date format
can be overridden through the `datefmt` parameter.

```python
import logging
from logfmter import Logfmter

formatter = Logfmter(
    keys=["at", "when"],
    mapping={"at": "levelname", "when": "asctime"},
    datefmt="%Y-%m-%d"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(handlers=[handler])

logging.error("hello") # at=ERROR when=2022-04-20 msg=hello
```

### Extend

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

logging.error({"example": True}) # at=ERROR example=yes
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
   $ git push origin main --tags
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
