"""Tests for base module."""

import json
import responses
from requests.exceptions import ConnectTimeout
import pytest
from pysolcast.base import PySolcast


BASE_URL = 'https://api.solcast.com.au'


def test_Solcast_init():
    """Test creating Solcast object."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    #endpoint = '/blah'

    # Act
    obj = PySolcast(api_key, resource_id)

    # Assert
    assert isinstance(obj, PySolcast)


@responses.activate
def test_get_data_200():
    """Test get_data."""
    # Arrange

    api_key = '12345'
    resource_id = '1234-1234'
    uri = '/blah'
    expected_url = f'{BASE_URL}{uri}'
    expected_response = """{}"""

    responses.add(
        responses.GET,
        expected_url,
        body=expected_response,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    obj = PySolcast(api_key, resource_id)
    response = obj._get_data(uri)  # pylint: disable=protected-access

    # Assert
    assert response == json.loads(expected_response)


@responses.activate
def test_get_data_timeout():
    """Test get_data with timeout."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    uri = '/blah'
    expected_url = f'{BASE_URL}{uri}'

    responses.add(
        responses.GET,
        expected_url,
        body=ConnectTimeout(),
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    obj = PySolcast(api_key, resource_id)
    with pytest.raises(ConnectTimeout):
        obj._get_data(uri)  # pylint: disable=protected-access

    # Assert


@responses.activate
def test_post_data():
    """Test post_measurements with 200 status code."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    endpoint = '/measurements'
    expected_url = f'{BASE_URL}{endpoint}'

    measurement_single = """{
        "measurement": {
            "period_end": "2018-02-02T03:30:00.0000000Z",
            "period": "PT5M",
            "total_power": 1.23456
        }
    }"""

    responses.add(
        responses.POST,
        expected_url,
        body=measurement_single,
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    obj = PySolcast(api_key, resource_id)
    measurement_response = obj._post_data(endpoint, measurement_single)  # pylint: disable=protected-access

    # Assert
    assert isinstance(measurement_response, dict)
    assert measurement_response == json.loads(measurement_single)


@responses.activate
def test_post_data_timeout():
    """Test post data with timeout."""
    # Arrange
    api_key = '12345'
    resource_id = '1234-1234'
    uri = '/blah'
    expected_url = f'{BASE_URL}{uri}'

    measurement_single = """{
        "measurement": {
            "period_end": "2018-02-02T03:30:00.0000000Z",
            "period": "PT5M",
            "total_power": 1.23456
        }
    }"""

    responses.add(
        responses.POST,
        expected_url,
        body=ConnectTimeout(),
        status=200,
        content_type='applicaiton/json'
    )

    # Act
    obj = PySolcast(api_key, resource_id)
    with pytest.raises(ConnectTimeout):
        obj._post_data(uri, measurement_single)  # pylint: disable=protected-access

    # Assert
