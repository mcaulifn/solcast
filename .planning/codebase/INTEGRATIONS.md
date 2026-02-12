# External Integrations

**Analysis Date:** 2026-02-12

## APIs & External Services

**Solcast API:**
- Service: Solcast API (https://api.solcast.com.au)
- Purpose: Solar forecasting and measurement data. Provides:
  - Rooftop site forecasts, estimated actuals, and measurements
  - Weather site forecasts and estimated actuals
  - Utility-scale site forecasts, estimated actuals, radiation data, and measurements
  - World solar radiation forecasts and estimated actuals
- SDK/Client: requests library (built-in HTTP client)
- Auth: API key authentication via HTTP Basic Auth (api_key as username, empty password)
  - Implementation: `pysolcast/base.py` lines 29, 52 use `auth=(self.api_key, '')`
  - API key: Passed as constructor argument to PySolcast subclasses

## Endpoints & Resources

**Available Endpoints:**
- `/rooftop_sites/{resource_id}/forecasts` - Get rooftop forecasts
- `/rooftop_sites/{resource_id}/estimated_actuals` - Get rooftop estimated actuals
- `/rooftop_sites/{resource_id}/measurements` - Post rooftop measurements
- `/weather_sites/{resource_id}/forecasts` - Get weather forecasts
- `/weather_sites/{resource_id}/estimated_actuals` - Get weather estimated actuals
- `/utility_scale_sites/{resource_id}/forecasts` - Get utility-scale forecasts
- `/utility_scale_sites/{resource_id}/estimated_actuals` - Get utility-scale estimated actuals
- `/utility_scale_sites/{resource_id}/measurements` - Post utility measurements
- `/utility_scale_sites/{resource_id}/weather/forecasts` - Get utility radiation forecasts
- `/utility_scale_sites/{resource_id}/weather/estimated_actuals` - Get utility radiation estimated actuals
- `/world_radiation/forecasts` - Get world radiation forecasts (location-based)
- `/world_radiation/estimated_actuals` - Get world radiation estimated actuals (location-based)

**Request/Response Format:**
- Format: JSON (specified via `format=json` parameter in requests)
- Response parsing: `_get_data()` and `_post_data()` return parsed JSON (`_get_response.json()` at line 34)

## Error Handling

**HTTP Status Codes:**
- 200: Success - returns JSON response
- 400: Validation Error - raises `ValidationError`
- 404: Site Error (site not found/not accessible) - raises `SiteError`
- 429: Rate Limit Exceeded - raises `RateLimitExceeded` with reset time from headers

**Connection Errors:**
- ConnectionError, Timeout: Re-raised after logging (lines 30-32, 53-55 in `base.py`)

**Rate Limiting:**
- Detection: HTTP 429 status code
- Rate limit reset info: Retrieved from `x-rate-limit-reset` response header
- Exception: `RateLimitExceeded` with reset time message

## Data Storage

**No Internal Database:**
- This is a client library only - no persistent storage
- Data is transient (in-memory API responses only)
- No database dependencies

## Client Classes by Site Type

**RooftopSite:** `pysolcast/rooftop.py`
- Extends: PySolcast
- Methods: get_forecasts(), get_forecasts_parsed(), get_estimated_actuals(), post_measurements()

**WeatherSite:** `pysolcast/weather.py`
- Extends: PySolcast
- Methods: get_forecasts(), get_estimated_actuals()

**UtilitySite:** `pysolcast/utility.py`
- Extends: PySolcast
- Methods: get_forecasts(), get_estimated_actuals(), get_radiation_forecasts(), get_radiation_estimated_actuals(), post_measurements()

**World:** `pysolcast/world.py`
- No resource_id required (overrides __init__)
- Methods: get_forecasts(latitude, longitude, hours), get_estimated_actuals(latitude, longitude, hours)

## Authentication & Identity

**Auth Provider:** Custom implementation (Solcast API)
- Implementation: HTTP Basic Authentication
  - Username: API key
  - Password: Empty string
  - Applied to all requests in `_get_data()` and `_post_data()` methods

**API Key Management:**
- Passed as constructor parameter: `PySolcast(api_key, resource_id)`
- No default/stored keys - must be provided at instantiation
- No environment variable support in library (caller responsibility)

## Data Parsing

**Date/Time Parsing:**
- Library: isodate 0.7.2
- Implementation: `parse_date_time()` function in `pysolcast/base.py` lines 68-76
- Converts ISO 8601 strings to Python datetime objects
- Parses ISO 8601 duration strings (e.g., "PT30M") to duration objects
- Applied to forecast data via `get_forecasts_parsed()` method in RooftopSite

**Configuration Parsing:**
- Library: anyconfig 0.14.0
- Purpose: Flexible configuration file handling (though not heavily used in core library)

## Monitoring & Observability

**Logging:**
- Framework: Python standard library `logging` module
- Logger: `logging.getLogger()` called in constructors (`base.py` line 20, `world.py` line 16)
- Log Levels:
  - info: Connection errors, rate limit events, API errors
  - No debug/warning/error levels explicitly used

**Error Logging Details:**
- Connection errors: Logged before re-raising (lines 31, 54)
- Rate limit: Logged with headers and response text (lines 36-38)
- Validation errors: Logged with headers (line 42)
- Site errors: Logged with headers (line 45)

**No External Monitoring:**
- No integration with error tracking services (Sentry, etc.)
- No metrics/tracing integration
- No external log aggregation

## CI/CD & Deployment

**Hosting:** PyPI package repository

**Build Process:**
- Build tool: Python build module (`python -m build`)
- Build backend: Poetry-core with poetry-dynamic-versioning
- SBOM generation: Anchore SBOM action (v0.21.0)
- Provenance: SLSA 3 via slsa-framework/slsa-github-generator v2.1.0

**CI Pipeline:** GitHub Actions (`.github/workflows/`)
- **pullrequest.yaml**: PR validation
  - Tests: tox across Python 3.9, 3.10, 3.11, 3.12
  - Linting: pylint via tox
  - Coverage: pytest-cov with Codecov upload
  - Code review: Dependency review action
  - SBOM generation: Anchore
  - Provenance: SLSA 3
  - Publish to Test PyPI

- **publish.yaml**: Release publishing
  - Triggers: On release creation or manual workflow_dispatch
  - Build: Creates distribution
  - Test PyPI: Pre-release publication
  - PyPI: Production publication (on git tags)
  - GitHub Release: Upload artifacts

- **codeql-analysis.yaml**: Security scanning via GitHub CodeQL

- **release.yaml**: Automated release management

**Coverage Requirements:**
- Target range: 70-100% (configured in `codecov.yml`)
- Tool: Codecov with pytest-cov
- Branch protection: Requires CI to pass on main branch

**Dependency Management:**
- Renovate: Automated dependency updates (configured in `renovate.json`)
- Policy: Auto-merge for linters and minor updates
- Dependency review: Required on PRs (fail on moderate severity)

## Package Publishing

**PyPI Publishing Workflow:**
1. Test PyPI publication on all PRs (`.github/workflows/pullrequest.yaml`)
2. Production PyPI publication on git tag creation (`.github/workflows/publish.yaml`)
3. Uses OIDC trusted publishing (no stored PyPI tokens)
4. Environment-based separation: testpypi and publish environments

**Version Management:**
- Dynamic versioning from git tags (setuptools-scm)
- Semantic Release (configured in `.releaserc.yaml`)
- Automatic version bumping based on commit types (angular preset)
- Release rules: major for breaking changes, patch for docs/refactor, no-release for certain types

---

*Integration audit: 2026-02-12*
