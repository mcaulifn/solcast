from requests import get, post
from requests.exceptions import ConnectionError, Timeout
import logging
import time
from solcast.exceptions import SiteNotFound, ValidationError, RateLimitExceeded


class Solcast:
    base_url = 'https://api.solcast.com.au'

    def __init__(self, api_key: str, resource_id: str):
        self.api_key = api_key
        self.resource_id = resource_id
        self.logger = logging.getLogger()

    def _get_data(self, uri: str) -> dict:
        url = f'{Solcast.base_url}{uri}'
        payload = {'format': 'json'}
        try:
            _get_response = get(url, auth=(self.api_key, ''), params=payload)
        except (ConnectionError, Timeout) as error:
            self.logger.info(error)
            raise error
        if _get_response.status_code == 200:
            return _get_response.json()
        if _get_response.status_code == 429:
            now = time.time()
            sleep_time = int(_get_response.headers.get('x-rate-limit-reset')) - now
            self.logger.info(f'Solcast API rate limit reached. Wait {sleep_time} seconds')
            raise RateLimitExceeded
        if _get_response.status_code == 400:
            raise ValidationError
        if _get_response.status_code == 404:
            raise SiteNotFound

    def _post_data(self, uri: str, data: dict) -> dict:
        url = f'{Solcast.base_url}{uri}'
        try:
            _post_response = post(url, data=data)
        except (ConnectionError, Timeout) as error:
            self.logger.info(error)
            raise error
        if _post_response.status_code == 200:
            return _post_response.json()
        if _post_response.status_code == 400:
            raise ValidationError
        if _post_response.status_code == 404:
            raise SiteNotFound

    def create_uri(self, uri, endpoint):
        return f'{uri}{self.resource_id}{endpoint}'
