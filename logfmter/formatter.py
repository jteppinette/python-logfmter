import logging
import numbers
from typing import Tuple

# Reserved log record attributes cannot be overwritten. They
# will not included in the formatted log.
#
# https://docs.python.org/3/library/logging.html#logrecord-attributes
RESERVED: Tuple[str, ...] = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
)


class Logfmter(logging.Formatter):
    @classmethod
    def format_string(cls, value: str) -> str:
        """
        Process the provided string with any necessary quoting and/or escaping.
        """
        needs_escaping = '"' in value
        needs_quoting = " " in value or "=" in value

        if needs_escaping:
            value = value.replace('"', '\\"')

        if needs_quoting:
            value = '"{}"'.format(value)

        return value if value else '""'

    @classmethod
    def format_value(cls, value) -> str:
        """
        Map the provided value to the proper logfmt formatted string.
        """
        if value is None:
            return ""
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, numbers.Number):
            return str(value)

        return cls.format_string(str(value))

    @classmethod
    def format_params(cls, params: dict) -> str:
        """
        Return a string representing the logfmt formatted parameters.
        """
        return " ".join(
            [
                "{}={}".format(key, cls.format_value(value))
                for key, value in params.items()
            ]
        )

    @classmethod
    def get_extra(cls, record: logging.LogRecord) -> dict:
        """
        Return a dictionary of logger extra parameters by filtering any reserved keys.
        """
        return {
            key: value for key, value in record.__dict__.items() if key not in RESERVED
        }

    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, dict):
            params = record.msg
        else:
            extra = self.get_extra(record)
            params = {"msg": record.getMessage(), **extra}

        return " ".join(
            (
                "at={}".format(record.levelname),
                self.format_params(params),
            )
        )
