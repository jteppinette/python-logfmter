# 0.0.8 (2024-05-24)

- Add official support for Python 3.12.

# 0.0.7 (2024-01-23)

- Improve documentation
- Add support for default key/value pairs provided via log record factory.
- Fix duplication issue that happened when keys/extras/msg values overlapped.

# 0.0.6 (2022-04-22)

- Improve documentation.
- Normalize keys to prevent users from breaking the logfmt style.

# 0.0.5 (2022-04-20)

- Add support for include native log record attributes in the final log output.
- Add support for overriding the date format used when formatting the `asctime` attribute.

# 0.0.4 (2022-03-29)

- Fix the usage documentation
- Escape newline characters in all logged values. Previously, you could generate
  multi-line log statements. This should never be the case.
- Add support for auto-generating `exc_info` parameters. If the log record is
  generated with `exc_info`, as in when using `logging.exception(...)`, the
  log message will contain properly formatted exception and traceback information.
- Add support for logging with an empty message dictionary.

# 0.0.3 (2022-01-13)

- Include type hints

# 0.0.1 (2022-01-06)

- Incept
