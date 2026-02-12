# Architecture

**Analysis Date:** 2026-02-12

## Pattern Overview

**Overall:** Inheritance-based API client library with polymorphic site types

**Key Characteristics:**
- Single-responsibility design with base class providing HTTP communication
- Multiple subclasses for different Solcast API endpoints (RooftopSite, WeatherSite, UtilitySite, World)
- Stateless request/response pattern with no persistence layer
- Exception-based error handling for API errors and validation failures

## Layers

**API Communication Layer:**
- Purpose: Encapsulates all HTTP interaction with Solcast API, handles authentication, error responses
- Location: `pysolcast/base.py`
- Contains: `PySolcast` base class with `_get_data()` and `_post_data()` methods
- Depends on: `requests` library, `isodate` for date parsing, custom exception classes
- Used by: All site-specific subclasses (RooftopSite, WeatherSite, UtilitySite, World)

**Site-Specific Resource Layer:**
- Purpose: Provide domain-specific methods for accessing forecasts, estimated actuals, and measurements for each site type
- Location: `pysolcast/rooftop.py`, `pysolcast/weather.py`, `pysolcast/utility.py`, `pysolcast/world.py`
- Contains: Resource-specific classes that extend PySolcast
- Depends on: Base class, helper functions like `parse_date_time()`
- Used by: Client code using the library

**Exception Handling Layer:**
- Purpose: Define custom exceptions for API errors and validation issues
- Location: `pysolcast/exceptions.py`
- Contains: `ValidationError`, `SiteError`, `RateLimitExceeded` exception classes
- Depends on: Python built-in Exception class
- Used by: Base class and subclasses for error signaling

**Utility Functions:**
- Purpose: Date/time parsing helpers for converting ISO 8601 strings to Python datetime objects
- Location: `pysolcast/base.py` (module-level `parse_date_time()` function)
- Contains: `parse_date_time()` function
- Depends on: `isodate` library
- Used by: RooftopSite for forecasts parsing

## Data Flow

**GET Request Flow (Fetch Forecasts):**

1. Client code calls site-specific method (e.g., `RooftopSite.get_forecasts()`)
2. Method constructs endpoint string and calls inherited `_get_data()`
3. `_get_data()` builds full URL, adds API key as Basic auth, makes HTTP GET request
4. Response status code is checked: 200 (success), 429 (rate limit), 400 (validation error), 404 (site error)
5. On success (200), JSON response is parsed and returned as dict
6. On error, appropriate exception is raised with error details

**POST Request Flow (Submit Measurements):**

1. Client code calls site-specific method (e.g., `RooftopSite.post_measurements()`)
2. Method constructs endpoint string and calls inherited `_post_data()` with data dict
3. `_post_data()` builds full URL, adds API key as Basic auth, makes HTTP POST request with JSON body
4. Response status code is checked: 200 (success), 400 (validation error), 404 (site error)
5. On success (200), JSON response is parsed and returned as dict
6. On error, exception is raised

**Parameterized Request Flow (Location-based Queries):**

1. Client code calls World class method with latitude/longitude (e.g., `World.get_forecasts()`)
2. Method builds params dict with location and optional filters
3. Method calls `_get_data()` with params argument
4. `_get_data()` merges params dict with base payload and passes as query parameters
5. Response is returned as-is or parsed

**State Management:**

- No persistent state: Each instance stores only API key and resource ID
- Stateless requests: No session state, caching, or connection pooling
- Each method call is independent and can be called in any order

## Key Abstractions

**PySolcast (Base Class):**
- Purpose: Abstract HTTP client for Solcast API with authentication and error handling
- Examples: `pysolcast/base.py` lines 12-76
- Pattern: Template method pattern - subclasses use inherited `_get_data()` and `_post_data()` to implement domain-specific endpoints
- Methods: `_get_data()`, `_post_data()`, `_create_uri()`

**Site Classes (RooftopSite, WeatherSite, UtilitySite):**
- Purpose: Site-specific API clients that inherit from PySolcast
- Examples: `pysolcast/rooftop.py`, `pysolcast/weather.py`, `pysolcast/utility.py`
- Pattern: Concrete implementations of the template method pattern
- Methods: Various `get_*()` methods that call inherited HTTP methods with appropriate endpoints and parameters

**World Class:**
- Purpose: Special case for location-based queries (no resource_id required)
- Examples: `pysolcast/world.py`
- Pattern: Inheritance with method override - overrides `__init__()` to not require resource_id, overrides `_create_uri()` to not use resource_id
- Methods: `get_forecasts()`, `get_estimated_actuals()`

**URI Construction:**
- Purpose: Build API endpoint paths from base URI, resource ID, and endpoint names
- Pattern: `_create_uri()` method standardizes URI building across site types
- Implementation: Most classes use `/{{base_uri}}/{{resource_id}}/{{endpoint}}`, World class uses `/{{base_uri}}/{{endpoint}}`

## Entry Points

**RooftopSite:**
- Location: `pysolcast/rooftop.py` lines 5-53
- Triggers: Client imports and instantiates with API key and resource ID
- Responsibilities: Provides forecasts, estimated actuals, and measurement submission for rooftop PV sites

**WeatherSite:**
- Location: `pysolcast/weather.py` lines 5-31
- Triggers: Client imports and instantiates with API key and resource ID
- Responsibilities: Provides forecasts and estimated actuals for weather sites

**UtilitySite:**
- Location: `pysolcast/utility.py` lines 5-82
- Triggers: Client imports and instantiates with API key and resource ID
- Responsibilities: Provides forecasts, estimated actuals, radiation data, and measurement submission for utility-scale sites

**World:**
- Location: `pysolcast/world.py` lines 6-58
- Triggers: Client imports and instantiates with API key only (no resource_id)
- Responsibilities: Provides location-based forecasts and actuals using latitude/longitude

## Error Handling

**Strategy:** Exception-based error handling with custom exception types for different error categories

**Patterns:**

**HTTP Status Code Mapping (in `_get_data()` and `_post_data()`):**
- 200: Success - parse and return JSON response
- 429: Rate limit exceeded - raise `RateLimitExceeded` with reset time from headers
- 400: Validation error - raise `ValidationError`
- 404: Site not found/not accessible - raise `SiteError`
- Connection/Timeout errors: Re-raise `requests.exceptions.ConnectionError` and `requests.exceptions.Timeout` directly

**Exception Classes:**
- `ValidationError`: Raised when API validation fails (400 status or validation issues)
- `SiteError`: Raised when site not found or inaccessible (404 status)
- `RateLimitExceeded`: Raised when rate limit hit (429 status), includes reset time

**Logging:**
- Errors are logged before being raised: `self.logger.info()` calls in base class
- Rate limit details logged with headers: `self.logger.info('headers: %s', _get_response.headers)`
- Connection errors logged before re-raise

## Cross-Cutting Concerns

**Logging:** Python's standard `logging` module, instantiated in `__init__()` as `self.logger = logging.getLogger()`. Used in base class for error logging and rate limit information.

**Validation:** Input validation is deferred to the Solcast API - client accepts parameters as-is and lets server validation return errors via 400 status code responses.

**Authentication:** HTTP Basic auth using API key and empty string as password. Implemented in `_get_data()` and `_post_data()` with `auth=(self.api_key, '')` parameter to requests.

**Timeout Handling:** Configurable per-request timeout (default 60 seconds) passed to requests.get() and requests.post(). Connection and timeout exceptions propagated to caller.

---

*Architecture analysis: 2026-02-12*
