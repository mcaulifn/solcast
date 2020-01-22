"""Exceptions Module."""


class ValidationError(Exception):  # pylint: disable=missing-class-docstring
    pass


class SiteNotFound(Exception):  # pylint: disable=missing-class-docstring
    pass


class RateLimitExceeded(Exception):  # pylint: disable=missing-class-docstring
    pass
