"""Tests for `WeatherSite` class."""

import responses
import pytest
from pysolcast.weather import WeatherSite
from pysolcast.exceptions import ValidationError, SiteError, RateLimitExceeded

BASE_URL = 'https://api.solcast.com.au'
WEATHER_URI = 'weather_sites'


def test_RooftopSite():
    """Test creating object."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'

    # Act
    site = WeatherSite(api_key, resource_id)

    # Assert
    assert isinstance(site, WeatherSite)


@responses.activate
def test_get_forecasts_200():
    """Test get_forecasts with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    forecast_response = {
        "forecasts": [
            {
                "ghi": "10",
                "ghi90": "12",
                "ghi10": "8",
                "ebh": "10",
                "dni": "10",
                "dni90": "12",
                "dni10": "8",
                "air_temp": "20",
                "zenith": "90",
                "azimuth": "45.1234",
                "cloud_opacity": "12",
                "period_end": "2018-01-01T01:00:00.00000Z",
                "period": "PT30"
            },
            {
                "ghi": "10",
                "ghi90": "12",
                "ghi10": "8",
                "ebh": "10",
                "dni": "10",
                "dni90": "12",
                "dni10": "8",
                "air_temp": "20",
                "zenith": "90",
                "azimuth": "45.1234",
                "cloud_opacity": "12",
                "period_end": "2018-01-01T12:30:00.00000Z",
                "period": "PT30"
            }
        ]
    }

    responses.add(
        responses.GET,
        expected_url,
        json=forecast_response,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    forecasts = site.get_forecasts()

    # Assert
    assert isinstance(forecasts, dict)
    assert len(forecasts['forecasts']) == 2


@responses.activate
def test_get_forecasts_400():
    """Test get_forecasts with 400 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(ValidationError):
        site.get_forecasts()

    # Assert


@responses.activate
def test_get_forecasts_404():
    """Test get_forecasts with 400 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(SiteError):
        site.get_forecasts()

    # Assert


@responses.activate
def test_get_forecasts_429():
    """Test get_forecasts with 429 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }

    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers)

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(RateLimitExceeded):
        site.get_forecasts()

    # Assert


@responses.activate
def test_get_estimated_actuals_200():
    """Test get_estimated_actuals with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'estimated_actuals'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    estimated_actual_response = {
        "estimated_actuals": [
            {
                "ghi": "10",
                "ebh": "10",
                "dni": "10",
                "dhi": "10",
                "cloud_opacity": "12",
                "period_end": "2018-01-01T01:05:00.00000Z",
                "period": "PT5M"
            },
            {
                "ghi": "10",
                "ebh": "10",
                "dni": "10",
                "dhi": "10",
                "cloud_opacity": "12",
                "period_end": "2018-01-01T01:00:00.00000Z",
                "period": "PT5M"
            }
        ]
    }

    responses.add(
        responses.GET,
        expected_url,
        json=estimated_actual_response,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    estimated_actuals = site.get_estimated_actuals()

    # Assert
    assert isinstance(estimated_actuals, dict)
    assert len(estimated_actuals['estimated_actuals']) == 2


@responses.activate
def test_get_estimated_actuals_400():
    """Test get_estimated_actuals with 400 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'estimated_actuals'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(ValidationError):
        site.get_estimated_actuals()

    # Assert


@responses.activate
def test_get_estimated_actuals_404():
    """Test get_estimated_actuals with 404 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'estimated_actuals'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(SiteError):
        site.get_estimated_actuals()

    # Assert


@responses.activate
def test_get_estimated_actuals_429():
    """Test get_estimated_actuals with 429 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'estimated_actuals'
    expected_url = f'{BASE_URL}/{WEATHER_URI}/{resource_id}/{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }
    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers
    )

    # Act
    site = WeatherSite(api_key, resource_id)
    with pytest.raises(RateLimitExceeded):
        site.get_estimated_actuals()

    # Assert
