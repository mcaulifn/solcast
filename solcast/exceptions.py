"""Exceptions Module."""


class ValidationError(Exception):  # pylint: disable=missing-class-docstring
    """Data validation error."""


class SiteError(Exception):  # pylint: disable=missing-class-docstring
    """Site Error.

    Site is not found or not accessable.
    """


class RateLimitExceeded(Exception):  # pylint: disable=missing-class-docstring
    """Rate limit exceeded."""
