# Technology Stack

**Analysis Date:** 2026-02-12

## Languages

**Primary:**
- Python 3.9+ - Core library implementation
- Python 3.10, 3.11, 3.12 - Tested versions (CI matrix in `pullrequest.yaml`)

## Runtime

**Environment:**
- Python 3.9+ (specified in `pyproject.toml`)
- Supports CPython 3.9, 3.10, 3.11, 3.12

**Package Manager:**
- Poetry 1.7.1 - Defined in `pyproject.toml`
- Lockfile: `poetry.lock` (present)

## Frameworks

**Core:**
- requests 2.31.0+ - HTTP client for API communication (`pysolcast/base.py`)

**Testing:**
- pytest 8.4.2 - Test runner
- pytest-cov 6.3.0 - Coverage reporting
- mock 5.2.0 - Mocking framework
- responses 0.25.8 - HTTP response mocking for tests (used in `tests/test_base.py`, `tests/test_rooftop.py`)

**Build/Dev:**
- Poetry-core >= 1.9.0 - Build backend
- poetry-dynamic-versioning >= 1.0.0, < 2.0.0 - Version management
- Sphinx 7.4.7 - Documentation generation
- sphinx-autodoc-typehints 2.3.0 - Type hints in Sphinx docs

## Key Dependencies

**Critical:**
- requests 2.31.0+ - HTTP communication with Solcast API
- isodate 0.7.2 - ISO 8601 date/time parsing (`pysolcast/base.py` line 6, used in `parse_date_time()`)
- anyconfig 0.14.0 - Configuration handling

**Code Quality:**
- pylint 3.3.9 - Linting (`tox.ini` pylint environment)
- pycodestyle 2.14.0 - PEP 8 style checking
- pydocstyle 6.3.0 - Docstring style validation
- autopep8 2.3.2 - Automatic PEP 8 formatting
- rope 1.14.0 - Refactoring library
- black 2.x - Code formatting (configured in `pyproject.toml` with max-line-length 120)

**Documentation:**
- Sphinx 7.4.7 - Technical documentation generation
- sphinx-autodoc-typehints 2.3.0 - Type hint documentation

**Version Management:**
- bump2version 1.0.1 - Version bumping
- setuptools-scm 8.3.1 - SCM version management

**Testing Support:**
- tox 4.25.0 - Test environment management (configured in `tox.ini` with py38, py39, py310, py311 environments)

## Configuration

**Environment:**
- Configuration via environment variables or code initialization
- API key and resource_id passed to class constructors (`pysolcast/base.py` lines 17-19)
- Base URL: `https://api.solcast.com.au` (hardcoded in `PySolcast.base_url`)

**Build:**
- `pyproject.toml` - Poetry project configuration with dependencies and build settings
- `tox.ini` - Test environment configuration (Python 3.8-3.11 testing)
- `poetry.lock` - Locked dependency versions

**Code Quality:**
- `.editorconfig` - Editor formatting rules (4-space indentation, UTF-8, LF line endings)
- Black configuration in `pyproject.toml` (max-line-length: 120)
- Poetry dynamic versioning enabled with bump=true in `pyproject.toml`

## Platform Requirements

**Development:**
- Python 3.9 or higher
- Poetry 1.7.1+ for dependency management
- tox for running test matrix across Python versions
- Git for version control (setuptools-scm reads from git)

**Production:**
- Python 3.9+ runtime
- requests library for HTTP communication
- isodate for date/time parsing
- anyconfig for configuration management
- Published to PyPI as `pysolcast` package

**CI/CD:**
- GitHub Actions workflows in `.github/workflows/`
- Ubuntu-latest runner for all workflows
- SLSA 3 provenance generation via slsa-framework/slsa-github-generator v2.1.0
- Codecov integration for coverage reporting

## Publishing & Release

**Package Repository:**
- PyPI - Primary production package repository
- Test PyPI - Pre-release testing environment (configured in `publish.yaml` and `pullrequest.yaml`)

**Versioning Strategy:**
- Semantic Release (configured in `.releaserc.yaml`)
- Dynamic versioning from git tags via setuptools-scm
- Automatic version bumping on release commits

---

*Stack analysis: 2026-02-12*
