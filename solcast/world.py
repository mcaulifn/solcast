"""World Solar Radiation module."""
import logging
from solcast.base import Solcast


class World(Solcast):
    """Class for interacting world solar radiation."""

    base_uri = 'world_radiation'

    def __init__(self, api_key):
        self.api_key = api_key
        self.logger = logging.getLogger()

    def get_forecasts(self, latitude, longitude, hours=None):
        """Get forecasts data for given location."""
        endpoint = 'forecasts'
        payload = {
            'latitude': latitude,
            'longitude': longitude,
            'hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def get_estimated_actuals(self, latitude, longitude, hours=None):
        """Get estimated actuals data for given location."""
        endpoint = 'estimated_actuals'
        payload = {
            'latitude': latitude,
            'longitude': longitude,
            'hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def create_uri(self, uri, endpoint) -> str:
        """Create a URI for specific endpoint."""
        return f'/{uri}/{endpoint}'
