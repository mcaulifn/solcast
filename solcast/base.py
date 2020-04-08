"""Base class"""
import logging
#import time
from isodate import parse_datetime, parse_duration
from requests import get, post
import requests.exceptions
from solcast.exceptions import SiteError, ValidationError, RateLimitExceeded


class Solcast:  # pylint: disable=too-few-public-methods
    """Base object."""
    base_url = 'https://api.solcast.com.au'

    def __init__(self, api_key: str, resource_id: str):
        self.api_key = api_key
        self.resource_id = resource_id
        self.logger = logging.getLogger()

    def _get_data(self, uri: str, params: dict = None) -> dict:  # pylint: disable=inconsistent-return-statements
        """Get data from API."""
        url = f'{Solcast.base_url}{uri}'
        payload = {'format': 'json'}
        if params:
            payload = {**payload, **params}
        try:
            _get_response = get(url, auth=(self.api_key, ''), params=payload)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            self.logger.info(f'Error getting data: {error}')  # pylint: disable=logging-format-interpolation
            raise error
        if _get_response.status_code == 200:
            return _get_response.json()
        if _get_response.status_code == 429:
            self.logger.info('Solcast API rate limit reached.')
            self.logger.info('headers: %s', _get_response.headers)
            self.logger.info('text: %s', _get_response.text)
            raise RateLimitExceeded(
                f"Rate limit exceeded. Reset time: {_get_response.headers.get('x-rate-limit-reset')}")  # pylint: disable=line-too-long
        if _get_response.status_code == 400:
            self.logger.info(  # pylint: disable=logging-format-interpolation
                f'Validation error: {_get_response.headers}')
            raise ValidationError('Validation error')
        if _get_response.status_code == 404:
            self.logger.info(f'Site error: {_get_response.headers}')  # pylint: disable=logging-format-interpolation
            raise SiteError('Site error')

    def _post_data(self, uri: str, data: dict) -> dict:  # pylint: disable=inconsistent-return-statements
        """Post data to API."""
        url = f'{Solcast.base_url}{uri}'
        try:
            _post_response = post(url, data=data)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            self.logger.info(error)
            raise error
        if _post_response.status_code == 200:
            return _post_response.json()
        if _post_response.status_code == 400:
            raise ValidationError
        if _post_response.status_code == 404:
            raise SiteError

    def _create_uri(self, uri: str, endpoint: str) -> str:
        """Create a URI for specific endpoint."""
        return f'/{uri}/{self.resource_id}/{endpoint}'


def parse_date_time(dic: dict, tld_key: str) -> dict:
    """Parse datetime and duration objects."""
    for item in dic[tld_key]:
        for key, value in item.items():
            if key == 'period_end':
                item[key] = parse_datetime(value)
            if key == 'period':
                item[key] = parse_duration(value)
    return dic
