# Codebase Concerns

**Analysis Date:** 2026-02-12

## Error Handling

**Incomplete return path handling:**
- Issue: Methods `_get_data` and `_post_data` in `pysolcast/base.py` marked with `# pylint: disable=inconsistent-return-statements`. These methods only explicitly return on success (status 200) or specific error codes (400, 404, 429). Any other HTTP status code will result in implicit `None` return rather than raising an exception.
- Files: `pysolcast/base.py` (lines 22, 48)
- Impact: Callers receive `None` on unexpected status codes without raising errors, leading to silent failures when API returns unexpected responses (e.g., 500, 502, 503, 503).
- Fix approach: Add a catch-all error handler for unhandled status codes or explicitly raise an exception for any status code not in {200, 400, 404, 429}.

**Inconsistent exception instantiation:**
- Issue: In `_post_data` method (line 59-61), `ValidationError` and `SiteError` are raised without arguments, while in `_get_data` method (lines 39, 43, 46) they are raised with descriptive error messages.
- Files: `pysolcast/base.py` (lines 59-61 vs 39, 43, 46)
- Impact: Inconsistent error context makes debugging difficult. POST failures provide no information about what went wrong.
- Fix approach: Standardize exception instantiation to include descriptive messages across all error scenarios.

## Design Issues

**World class violates inheritance contract:**
- Issue: `World.__init__` does not call `super().__init__()` as indicated by `# pylint: disable=super-init-not-called` comment on line 14. It manually initializes `api_key` and `logger` but skips `resource_id`. This violates the parent class contract.
- Files: `pysolcast/world.py` (line 14)
- Impact: World class is fundamentally different from other site classes as it doesn't use `resource_id`. This is correct for the API, but the inheritance structure is misleading. If parent class initializer changes, World class initialization could break.
- Fix approach: Either make World not inherit from PySolcast, or override `__init__` cleanly without relying on parent initialization. Consider composition over inheritance.

**Pylint suppressions indicate design problems:**
- Issue: Multiple design-focused pylint suppressions suggest underlying architectural issues:
  - `too-few-public-methods`: `PySolcast` class only has 3 public methods, suggesting it's more of a data container than a proper base class.
  - `super-init-not-called`: World class doesn't properly initialize parent.
  - `inconsistent-return-statements`: Methods lack proper error handling paths.
- Files: `pysolcast/base.py`, `pysolcast/world.py`
- Impact: These suppressions mask underlying design problems rather than solving them.
- Fix approach: Refactor base class design to be cleaner. Consider making PySolcast a utility class or mixin rather than a traditional base class.

## API Request Issues

**Default timeout is hardcoded:**
- Issue: Both `_get_data` (line 22) and `_post_data` (line 48) have a default timeout of 60 seconds hardcoded in the signature. This is not configurable per-instance.
- Files: `pysolcast/base.py` (lines 22, 48)
- Impact: Users cannot adjust timeout globally or per-site. Long-running API requests cannot be configured. No way to use different timeouts for different request types.
- Fix approach: Make timeout configurable at instance initialization or provide class-level configuration.

**Basic Auth credentials in logs:**
- Issue: While the code correctly uses `auth=(self.api_key, '')` for requests, the API key is stored as instance variable and printed in logs via logging statements (lines 31, 54). If logs are ever captured or reviewed, API key is visible.
- Files: `pysolcast/base.py` (lines 31, 54)
- Impact: Potential credential exposure if logs are captured, archived, or reviewed.
- Fix approach: Never log the API key. Use sanitization in logging statements or structured logging that masks sensitive fields.

## Data Parsing

**Hardcoded dictionary key assumptions:**
- Issue: `parse_date_time` function assumes the response always has the specified `tld_key` and that items in that array exist. No validation or error handling.
- Files: `pysolcast/base.py` (lines 68-76)
- Impact: If API response format changes or is missing expected key, function crashes with KeyError. If `tld_key` is empty list, function silently succeeds with no parsing done.
- Fix approach: Add validation for key existence. Provide meaningful error messages if structure is unexpected. Handle empty arrays.

**parse_date_time modifies input in-place:**
- Issue: Function modifies the dictionary passed to it in-place (line 71: `item[key] = parse_datetime(value)`). This is not obvious from the function signature and could surprise callers.
- Files: `pysolcast/base.py` (line 71)
- Impact: Unexpected mutation of caller's data. If a caller expects the original data to remain unchanged, this breaks that expectation.
- Fix approach: Return a new dictionary or clearly document the mutation behavior.

## Test Coverage Gaps

**Missing error handling tests:**
- What's not tested: POST request failures with 400 and 404 status codes are not tested. Only 200 is tested for successful POST.
- Files: `tests/test_base.py` (lines 82-113 only test success case for POST), `tests/test_rooftop.py`, `tests/test_utility.py`, `tests/test_weather.py`
- Risk: POST error responses are not validated. Changes to error handling in `_post_data` could break silently.
- Priority: High

**Missing parse_date_time tests:**
- What's not tested: The `parse_date_time` utility function has no dedicated tests. Only indirectly tested through `get_forecasts_parsed`.
- Files: `pysolcast/base.py` (lines 68-76) - not explicitly tested in `tests/`
- Risk: Changes to parsing logic could break forecasts unexpectedly. Invalid API responses could cause crashes without test coverage.
- Priority: High

**Incomplete World class testing:**
- What's not tested: World class methods don't have tests for 400 and 404 errors like other site classes, only 200 and 429 are tested.
- Files: `tests/test_world.py` (missing 400, 404 error cases)
- Risk: Error handling differences from other site classes are not validated.
- Priority: Medium

**API timeout behavior not tested:**
- What's not tested: Timeout handling. Both `_get_data` and `_post_data` accept timeout parameter but no tests verify timeout behavior.
- Files: `pysolcast/base.py` (lines 22, 48)
- Risk: Changes to timeout handling could break without detection.
- Priority: Medium

## Code Quality

**Inconsistent f-string vs percent formatting:**
- Issue: Logging uses inconsistent styles. Line 31 uses f-string, but lines 37-38, 42, 45 use percent-style formatting.
- Files: `pysolcast/base.py` (lines 31 vs 37-38, 42, 45)
- Impact: Inconsistent code style. F-string logging with logger is also flagged by pylint for performance reasons.
- Fix approach: Use percent-style formatting consistently for logging (more efficient and recommended for loggers).

**Typo in exception instantiation:**
- Issue: Line 59 raises `ValidationError` without message, while line 43 raises it with message. This is not a typo but inconsistent.
- Files: `pysolcast/base.py` (line 59 vs 43)
- Impact: Inconsistent error information.
- Fix approach: Standardize message passing.

## Security Considerations

**Authentication method vulnerability:**
- Risk: Uses Basic Auth with empty password. While this is technically the Solcast API requirement, it means the entire API key is the username. If intercepted (even over HTTPS), the key is exposed.
- Files: `pysolcast/base.py` (lines 29, 52)
- Current mitigation: Uses HTTPS by default (url starts with https://). API key must be kept secret in environment.
- Recommendations: Document clearly that API key must be treated as a secret. Consider supporting token-based auth if Solcast API adds it.

**No certificate verification control:**
- Risk: The requests library is used with default SSL verification, but there's no way for users to disable it (which could be needed for some corporate proxies, though risky).
- Files: `pysolcast/base.py` (lines 29, 52)
- Current mitigation: Default SSL verification is on.
- Recommendations: This is acceptable for security. Keep as-is.

## Fragile Areas

**BaseURL hardcoding:**
- Files: `pysolcast/base.py` (line 15)
- Why fragile: The base URL is hardcoded as a class variable. If Solcast changes their API endpoint, all instances need code changes. Not configurable.
- Safe modification: Add instance or class-level configuration for base_url.
- Test coverage: No tests verify correct base URL usage; tests mock responses so endpoint changes wouldn't be caught.

**Response parsing is tightly coupled:**
- Files: `pysolcast/base.py` (_get_data and _post_data), individual site classes
- Why fragile: Each site class method returns raw dictionary response. Any changes to API response format require code changes. No data validation or schema checking.
- Safe modification: Add response validation schema. Consider using dataclasses or Pydantic models for type safety.
- Test coverage: Tests use hardcoded response dictionaries, so new API fields or missing fields aren't validated.

**Parameter passing inconsistency:**
- Files: `pysolcast/utility.py` (methods accept period and hours as parameters), `pysolcast/rooftop.py` (methods accept params dict)
- Why fragile: Different site classes have different parameter passing conventions. UtilitySite requires explicit period/hours, RooftopSite uses optional params dict.
- Safe modification: Standardize parameter handling across all site classes.
- Test coverage: Tests only verify happy path with correct parameters.

## Dependencies at Risk

**requests library version constraint:**
- Risk: Uses `requests = "^2.31.0"` which allows minor/patch updates. Recent versions (2.31.1+) might have breaking changes not caught.
- Impact: Any breaking change in requests library could break the package.
- Migration plan: Monitor requests changelog. Consider pinning to exact version if stability is critical.

---

*Concerns audit: 2026-02-12*
