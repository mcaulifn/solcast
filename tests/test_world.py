"""Tests for World class."""

import responses
import pytest
from pysolcast.world import World
from pysolcast.exceptions import ValidationError, SiteError, RateLimitExceeded

BASE_URL = 'https://api.solcast.com.au'
WORLD_URI = '/world_radiation/'


def test_World():
    """Test creating object."""
    # Arrange
    api_key = '12345'

    # Act
    site = World(api_key)

    # Assert
    assert isinstance(site, World)


@responses.activate
def test_get_forecasts_200():
    """Test get_forecasts with 200 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'forecasts'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    forecast_response = {
        "forecasts": [
            {
                "ghi": 690,
                "ghi90": 802,
                "ghi10": 537,
                "period_end": "2017-01-30T05:00:00.0000000Z",
                "period": "PT30M"
            },
            {
                "ghi": 422,
                "ghi90": 707,
                "ghi10": 141,
                "period_end": "2017-01-30T05:30:00.0000000Z",
                "period": "PT30M"
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
    site = World(api_key)
    forecasts = site.get_forecasts(latitude, longitude)

    # Assert
    assert isinstance(forecasts, dict)
    assert len(forecasts['forecasts']) == 2


@responses.activate
def test_get_forecasts_400():
    """Test get_forecasts with 400 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'forecasts'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = World(api_key)
    with pytest.raises(ValidationError):
        site.get_forecasts(latitude, longitude)

    # Assert


@responses.activate
def test_get_forecasts_404():
    """Test get_forecasts with 400 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'forecasts'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = World(api_key)
    with pytest.raises(SiteError):
        site.get_forecasts(latitude, longitude)

    # Assert


@responses.activate
def test_get_forecasts_429():
    """Test get_forecasts with 429 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'forecasts'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }

    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers)

    # Act
    site = World(api_key)
    with pytest.raises(RateLimitExceeded):
        site.get_forecasts(latitude, longitude)

    # Assert


@responses.activate
def test_get_estimated_actuals_200():
    """Test get_estimated_actuals with 200 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'estimated_actuals'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    estimated_actual_response = {
        "estimated_actuals": [
            {
                "ghi": 640,
                "ebh": 516,
                "dni": 803,
                "dhi": 124,
                "cloud_opacity": 0,
                "period_end": "2017-01-29T23:00:00.0000000Z",
                "period": "PT30M"
            },
            {
                "ghi": 543,
                "ebh": 430,
                "dni": 769,
                "dhi": 113,
                "cloud_opacity": 0,
                "period_end": "2017-01-29T22:30:00.0000000Z",
                "period": "PT30M"
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
    site = World(api_key)
    estimated_actuals = site.get_estimated_actuals(latitude, longitude)

    # Assert
    assert isinstance(estimated_actuals, dict)
    assert len(estimated_actuals['estimated_actuals']) == 2


@responses.activate
def test_get_estimated_actuals_400():
    """Test get_estimated_actuals with 400 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'estimated_actuals'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = World(api_key)
    with pytest.raises(ValidationError):
        site.get_estimated_actuals(latitude, longitude)

    # Assert


@responses.activate
def test_get_estimated_actuals_404():
    """Test get_estimated_actuals with 404 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'estimated_actuals'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = World(api_key)
    with pytest.raises(SiteError):
        site.get_estimated_actuals(latitude, longitude)

    # Assert


@responses.activate
def test_get_estimated_actuals_429():
    """Test get_estimated_actuals with 429 status code."""
    # Arrange
    api_key = '12345'
    endpoint = 'estimated_actuals'
    latitude = '-35.123'
    longitude = '149.123'
    expected_url = f'{BASE_URL}{WORLD_URI}{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }
    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers
    )

    # Act
    site = World(api_key)
    with pytest.raises(RateLimitExceeded):
        site.get_estimated_actuals(latitude, longitude)

    # Assert
