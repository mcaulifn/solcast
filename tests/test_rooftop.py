"""Tests for `RoofTopSite` class."""

import responses
import pytest
from pysolcast.rooftop import RooftopSite
from pysolcast.exceptions import ValidationError, SiteError, RateLimitExceeded

BASE_URL = 'https://api.solcast.com.au'
ROOFTOP_URI = 'rooftop_sites'


def test_RooftopSite():
    """Test creating object."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'

    # Act
    site = RooftopSite(api_key, resource_id)

    # Assert
    assert isinstance(site, RooftopSite)


@responses.activate
def test_get_forecasts_200():
    """Test get_forecasts with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

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

    responses.add(
        responses.GET,
        expected_url,
        json=forecast_response,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts()

    # Assert
    assert isinstance(forecasts, dict)
    assert len(forecasts['forecasts']) == 2


@responses.activate
def test_get_forecasts_parsed_200():
    """Test get_forecasts_parsed with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'forecasts'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

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

    responses.add(
        responses.GET,
        expected_url,
        json=forecast_response,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    forecasts = site.get_forecasts_parsed()

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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }

    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers)

    # Act
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    estimated_actual_response = {
        "estimated_actuals": [
            {
                "pv_estimate": "10",
                "period_end": "2018-01-01T01:00:00.00000Z",
                "period": "PT30M"
            },
            {
                "pv_estimate": "9",
                "period_end": "2018-01-01T12:30:00.00000Z",
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
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=400
    )

    # Act
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    responses.add(
        responses.GET, expected_url, status=404
    )

    # Act
    site = RooftopSite(api_key, resource_id)
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
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'
    headers = {
        'x-rate-limit-reset': '155555555'
    }
    responses.add(
        responses.GET, expected_url, status=429, adding_headers=headers
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    with pytest.raises(RateLimitExceeded):
        site.get_estimated_actuals()

    # Assert


@responses.activate
def test_post_measurements_single():
    """Test post_measurements with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'measurements'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'

    measurement_single = {
        "measurement": {
            "period_end": "2018-02-02T03:30:00.0000000Z",
            "period": "PT5M",
            "total_power": 1.23456
        }
    }

    responses.add(
        responses.POST,
        expected_url,
        json=measurement_single,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    measurement_response = site.post_measurements(measurement_single)

    # Assert
    assert isinstance(measurement_response, dict)
    assert measurement_response == measurement_single


@responses.activate
def test_post_measurements_400():
    """Test post_measurements with 400 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'measurements'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'
    measurement_single = {
        "measurement": {
            "period_end": "2018-02-02T03:30:00.0000000Z",
            "period": "PT5M",
            "total_power": 1.23456
        }
    }

    responses.add(
        responses.POST, expected_url, status=400
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    with pytest.raises(ValidationError):
        site.post_measurements(measurement_single)

    # Assert


@responses.activate
def test_post_measurements_404():
    """Test post_measurements with 404 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = 'measurements'
    expected_url = f'{BASE_URL}/{ROOFTOP_URI}/{resource_id}/{endpoint}'
    measurement_single = {
        "measurement": {
            "period_end": "2018-02-02T03:30:00.0000000Z",
            "period": "PT5M",
            "total_power": 1.23456
        }
    }

    responses.add(
        responses.POST, expected_url, status=404
    )

    # Act
    site = RooftopSite(api_key, resource_id)
    with pytest.raises(SiteError):
        site.post_measurements(measurement_single)

    # Assert
