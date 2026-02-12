# Coding Conventions

**Analysis Date:** 2026-02-12

## Naming Patterns

**Files:**
- Lowercase with underscores for module files: `base.py`, `rooftop.py`, `utility.py`, `weather.py`, `world.py`, `exceptions.py`
- Lowercase with underscores for test files: `test_base.py`, `test_rooftop.py`, `test_utility.py`, `test_weather.py`, `test_world.py`

**Classes:**
- PascalCase for class names: `PySolcast`, `RooftopSite`, `UtilitySite`, `WeatherSite`, `World`
- Exception classes in PascalCase: `ValidationError`, `SiteError`, `RateLimitExceeded`

**Functions:**
- snake_case for function names: `get_forecasts()`, `get_estimated_actuals()`, `post_measurements()`, `parse_date_time()`, `_get_data()`, `_post_data()`, `_create_uri()`
- Private functions prefixed with single underscore: `_get_data()`, `_post_data()`, `_create_uri()`
- Public API methods use descriptive get/post pattern: `get_forecasts()`, `post_measurements()`

**Variables:**
- snake_case for all variables: `api_key`, `resource_id`, `base_url`, `expected_url`, `forecast_response`, `period_end`, `tld_key`
- Local module-level variables in UPPERCASE for constants: `BASE_URL`, `ROOFTOP_URI`, `UTILTY_URI`, `WEATHER_URI`, `WORLD_URI`

**Types:**
- Type hints used throughout: `-> dict`, `-> str`, `uri: str`, `params: dict = None`
- Dictionary type hint used for JSON responses: `-> dict`

## Code Style

**Formatting:**
- 4-space indentation (configured in `.editorconfig`)
- Maximum line length of 120 characters (configured in `pyproject.toml` for Black)
- Trailing whitespace removed
- Final newline inserted in all files
- UTF-8 charset
- LF line endings

**Linting:**
- Pylint configured as code quality tool (run via `tox -e pylint`)
- Pycodestyle (PEP8) validation
- Pydocstyle for docstring validation
- Pylint disable comments used inline for acceptable violations: `# pylint: disable=too-few-public-methods`, `# pylint: disable=inconsistent-return-statements`, `# pylint: disable=super-init-not-called`, `# pylint: disable=protected-access`, `# pylint: disable=logging-fstring-interpolation`

## Import Organization

**Order:**
1. Standard library imports: `import logging`, `import json`
2. Third-party imports: `from isodate import parse_datetime, parse_duration`, `from requests import get, post`, `import requests.exceptions`, `import responses`, `import pytest`
3. Local/project imports: `from pysolcast.base import PySolcast`, `from pysolcast.exceptions import ...`

**Pattern:**
- Use specific imports rather than wildcard imports
- Group imports by category with blank lines between groups
- Import specific items needed: `from isodate import parse_datetime, parse_duration`

**Path Aliases:**
- Absolute imports using full module path: `from pysolcast.base import ...`
- No relative imports used

## Error Handling

**Patterns:**
- Custom exceptions defined in `pysolcast/exceptions.py`: `ValidationError`, `SiteError`, `RateLimitExceeded`
- HTTP status code mapped to exception types in `_get_data()` and `_post_data()` methods
  - 400 → `ValidationError`
  - 404 → `SiteError`
  - 429 → `RateLimitExceeded`
  - 200 → Success (return JSON response)
- Connection errors caught and re-raised: `except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error: raise error`
- Logging used for error information before raising exceptions

**Example from `pysolcast/base.py`:**
```python
try:
    _get_response = get(url, auth=(self.api_key, ''), params=payload, timeout=timeout)
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
    self.logger.info(f'Error getting data: {error}')
    raise error
if _get_response.status_code == 200:
    return _get_response.json()
if _get_response.status_code == 429:
    self.logger.info('Solcast API rate limit reached.')
    raise RateLimitExceeded(...)
```

## Logging

**Framework:** Python's built-in `logging` module

**Patterns:**
- Logger created per module: `self.logger = logging.getLogger()`
- Log level used is `info` for business events and errors
- Formatted logging with % operator: `self.logger.info('headers: %s', _get_response.headers)`
- F-strings avoided in logging calls (pylint rule disabled when necessary)

**Examples:**
```python
self.logger.info(f'Error getting data: {error}')  # With pylint disable for fstring
self.logger.info('Solcast API rate limit reached.')
self.logger.info('headers: %s', _get_response.headers)
```

## Comments

**When to Comment:**
- Module-level docstrings required for all files
- Class docstrings required with description and URL references to API docs
- Method docstrings required with parameters, return types, and raised exceptions using reST format
- Inline comments used sparingly, only for non-obvious logic
- `pylint: disable` comments used for acceptable deviations from linting rules

**Docstring Format:**
- Triple-quoted strings for all docstrings
- reST format (Sphinx compatible) for method documentation
- Parameter documentation: `:param name: description`
- Return documentation: `:return: description` or `:returns: description`
- Exception documentation: `:raises ExceptionType: description`

**Examples from `pysolcast/utility.py`:**
```python
def get_forecasts(self, period: str, hours: str) -> dict:
    """Get forecasts data for site.

    :param period: Length of the averaging period in ISO8601 duration format.
    :param hours: An offset to which the number of forecasts will be included in the response.
    :return: forecasts
    :raises SiteError:
    """
```

## Function Design

**Size:**
- Methods are typically short (5-30 lines) focused on single operations
- GET methods construct URI and payload, delegate to `_get_data()`
- POST methods construct URI and payload, delegate to `_post_data()`

**Parameters:**
- Type hints required for all parameters: `uri: str`, `params: dict = None`, `timeout=60`
- Parameters always lowercase snake_case
- Default parameters used for optional API parameters: `period: str = None`, `timeout=60`

**Return Values:**
- Type hint required: `-> dict` for JSON responses, `-> str` for string URIs
- Return JSON response directly (dict): `return _get_response.json()`
- Return constructed strings for URI building: `return f'/{uri}/{self.resource_id}/{endpoint}'`
- Methods with conditional logic may not return in all paths (pylint disabled): `# pylint: disable=inconsistent-return-statements`

## Module Design

**Exports:**
- Public classes exported implicitly (used in `pysolcast/__init__.py` or imported directly)
- No explicit `__all__` list used
- Private methods prefixed with underscore: `_get_data()`, `_post_data()`, `_create_uri()`

**Barrel Files:**
- `pysolcast/__init__.py` minimal, only module/author metadata
- Consumers import directly: `from pysolcast.rooftop import RooftopSite`

**Class Hierarchy:**
- Base class `PySolcast` in `pysolcast/base.py` provides common API functionality
- Site classes inherit from `PySolcast`: `RooftopSite(PySolcast)`, `UtilitySite(PySolcast)`, `WeatherSite(PySolcast)`
- `World` class uses partial inheritance (only `__init__` overridden) for non-site-specific operations
- Common methods `_get_data()`, `_post_data()`, `_create_uri()` defined in base class

---

*Convention analysis: 2026-02-12*
