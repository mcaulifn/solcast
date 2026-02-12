# Testing Patterns

**Analysis Date:** 2026-02-12

## Test Framework

**Runner:**
- pytest 8.4.2
- Config: Configured in `tox.ini` with `pytest` command
- Coverage tracking enabled via `pytest-cov`

**Assertion Library:**
- pytest's built-in assertions (assert statements)

**Run Commands:**
```bash
poetry run python -m pytest --cov=pysolcast --doctest-modules --cov-report=term-missing -l --junitxml=pytest-report.xml --cov-report xml:coverage.xml tests/
# Full test run via tox: tox
# Pytest directly: pytest
# Watch mode: Not configured
# Coverage report: Integrated in pytest command above, or view via coverage.xml
```

## Test File Organization

**Location:**
- Tests co-located in separate `tests/` directory (not co-located with source)
- Dedicated directory structure: `/tests/` mirrors source module organization

**Naming:**
- Test modules prefixed with `test_`: `test_base.py`, `test_rooftop.py`, `test_utility.py`, `test_weather.py`, `test_world.py`
- Test functions prefixed with `test_`: `test_Solcast_init()`, `test_get_data_200()`, `test_get_forecasts_200()`
- Test naming includes HTTP status codes for response tests: `test_get_forecasts_200()`, `test_get_forecasts_400()`, `test_get_forecasts_404()`, `test_get_forecasts_429()`

**Structure:**
```
tests/
├── __init__.py
├── test_base.py       # Tests for PySolcast base class
├── test_rooftop.py    # Tests for RooftopSite class
├── test_utility.py    # Tests for UtilitySite class
├── test_weather.py    # Tests for WeatherSite class
├── test_world.py      # Tests for World class
```

## Test Structure

**Suite Organization:**
- One test module per source module
- Tests group related functionality (e.g., all GET forecasts variants, all POST measurements variants)
- No explicit test classes; standalone test functions organized by feature

**Test function pattern:**
```python
def test_get_forecasts_200():
    """Test get_forecasts with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    forecast_response = {
        "forecasts": [...]
    }

    responses.add(
        responses.GET,
        expected_url,
        json=forecast_response,
        status=200,
        content_type='application/json'
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts()

    # Assert
    assert isinstance(forecasts, dict)
    assert len(forecasts['forecasts']) == 2
```

**Patterns:**
- **AAA Pattern:** All tests follow Arrange-Act-Assert structure with comments
  - Arrange: Set up test data, mocks, and fixtures
  - Act: Call the method/function being tested
  - Assert: Verify the results
- **Teardown pattern:** Not explicitly used; mocks auto-cleanup via decorator
- **Assertion pattern:** Simple assert statements with type checks and value assertions

## Mocking

**Framework:** `responses` library (v0.25.8) for mocking HTTP requests

**Patterns:**
```python
@responses.activate
def test_get_data_200():
    # Mock setup
    responses.add(
        responses.GET,
        expected_url,
        body=expected_response,
        status=200,
        content_type='application/json'
    )

    # Call actual method
    obj = PySolcast(api_key, resource_id)
    response = obj._get_data(uri)

    # Verify mock was called
    assert responses.calls[0].request.headers['Authorization'] == 'Basic MTIzNDU6'
```

**Decorator Usage:**
- `@responses.activate` decorator on each test that mocks HTTP responses
- Decorator enables request interception and mocking within test scope
- Example from `tests/test_base.py`:
```python
@responses.activate
def test_get_data_200():
    """Test get_data."""
    # ... test code
```

**What to Mock:**
- HTTP requests (all external API calls mocked with `responses`)
- Response status codes (200, 400, 404, 429 all tested)
- Response headers (e.g., rate limit headers in 429 tests)
- JSON response bodies
- Network exceptions: `ConnectTimeout` (from `requests.exceptions`)

**What NOT to Mock:**
- Class instantiation (direct instantiation used)
- Datetime/ISO date parsing (library functions tested indirectly)
- Dictionary operations
- String formatting and URI construction

## Fixtures and Factories

**Test Data:**
- Inline JSON response data defined in test functions
- Example response structure in `test_rooftop.py`:
```python
forecast_response = {
    "forecasts": [
        {
            "pv_estimate": "9.5",
            "pv_estimate10": "6",
            "pv_estimate90": "13.8",
            "period_end": "2018-01-01T01:00:00.00000Z",
            "period": "PT30M"
        },
        {
            "pv_estimate": "10",
            "pv_estimate10": "8",
            "pv_estimate90": "12",
            "period_end": "2018-01-01T12:30:00.00000Z",
            "period": "PT30M"
        }
    ]
}
```

**Test Constants:**
- Module-level constants for repeated test data
- `BASE_URL = 'https://api.solcast.com.au'`
- `ROOFTOP_URI = 'rooftop_sites'`
- `UTILTY_URI = 'utility_scale_sites'`
- `WEATHER_URI = 'weather_sites'`
- `WORLD_URI = '/world_radiation/'`

**Location:**
- No separate fixtures file
- All test data and mocks defined inline within test functions
- No use of pytest fixtures or conftest.py

## Coverage

**Requirements:**
- No explicit coverage threshold enforced
- Coverage reports generated: `--cov-report=term-missing` (terminal), `xml:coverage.xml` (XML for CI)

**View Coverage:**
```bash
poetry run python -m pytest --cov=pysolcast --cov-report=term-missing tests/
# Or via tox
tox
```

**Configuration in `.coveragerc`:**
```ini
[run]
omit =
    */tests*

[report]
exclude_lines =
    pass
show_missing = True
```

## Test Types

**Unit Tests:**
- All tests are unit tests
- Each test focuses on a single method/function
- Tests verify:
  - Successful API responses (200 status codes)
  - Error handling (400, 404, 429 status codes)
  - Exception raising
  - Request parameters and headers
  - Response data structure and type

**Example from `tests/test_rooftop.py`:**
```python
def test_RooftopSite():
    """Test creating object."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    # Act
    site = RooftopSite(api_key, resource_id)
    # Assert
    assert isinstance(site, RooftopSite)
```

**Integration Tests:**
- Not applicable; HTTP mocked via `responses` library
- Tests verify integration between class instantiation and HTTP request layers

**E2E Tests:**
- Not implemented
- External API calls always mocked in test suite

## Common Patterns

**Async Testing:**
- Not applicable; no async/await in codebase

**Error Testing:**
- HTTP status code testing pattern: one test per error status code
- Exception verification with `pytest.raises()`:
```python
@responses.activate
def test_get_forecasts_400():
    """Test get_forecasts with 400 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    with pytest.raises(ValidationError):
        site.get_forecasts()

    # Assert (implicit in pytest.raises context)
```

**Successful Response Testing:**
- One test per method with 200 status code
- Verifies response is dict, correct structure, data present
```python
assert isinstance(forecasts, dict)
assert len(forecasts['forecasts']) == 2
assert forecasts == expected_response
```

**Connection Error Testing:**
- Timeout and connection errors tested in base class tests
- `ConnectTimeout` exception raised by requests, caught and re-raised by implementation
```python
@responses.activate
def test_get_data_timeout():
    """Test get_data with timeout."""
    responses.add(
        responses.GET,
        expected_url,
        body=ConnectTimeout(),
        status=200,
    )
    obj = PySolcast(api_key, resource_id)
    with pytest.raises(ConnectTimeout):
        obj._get_data(uri)
```

## Test Statistics

- **Total test files:** 5 (test_base.py, test_rooftop.py, test_utility.py, test_weather.py, test_world.py)
- **Total test functions:** Approximately 50+ test functions
- **Lines of test code:** ~1,865 lines (majority of codebase)
- **Test-to-code ratio:** High (test code ~3x source code)

## Test Execution via Tox

**Tox configuration in `tox.ini`:**
- Python versions tested: py38, py39, py310, py311
- Test command includes:
  - `--cov=pysolcast` - Coverage for pysolcast module only
  - `--doctest-modules` - Run doctests in modules
  - `--cov-report=term-missing` - Show coverage report with missing lines
  - `-l` - Show local variables on failure
  - `--junitxml=pytest-report.xml` - JUnit XML output for CI
  - `--cov-report xml:coverage.xml` - XML coverage for CI

---

*Testing analysis: 2026-02-12*
