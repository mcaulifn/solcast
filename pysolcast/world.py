"""World Solar Radiation Module."""
import logging
from pysolcast.base import PySolcast


class World(PySolcast):
    """Class for interacting with world solar radiation endpoint.

    Refer to https://docs.solcast.com.au/#world-solar-radiation-data for more information.
    """

    base_uri = 'world_radiation'

    def __init__(self, api_key):  # pylint: disable=super-init-not-called
        self.api_key = api_key
        self.logger = logging.getLogger()

    def get_forecasts(self, latitude: str, longitude: str, hours: str = None) -> dict:
        """Get forecasts data for given location.

        :param latitude: The latitude of the location (EPSG:4326)
        :param longitude: The longitude of the location (EPSG:4326)
        :param hours: Time window of the response in hours
        :return: forecasts
        :raises ValidationError:
            Latitude, longitude or hours are invalid, see response_status for further details
        :raises SiteNotFound: The location is outside our coverage area.
        """
        endpoint = 'forecasts'
        payload = {
            'latitude': latitude,
            'longitude': longitude,
            'hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def get_estimated_actuals(self, latitude: str, longitude: str, hours: str = None) -> dict:
        """Get estimated actuals data for given location.

        :param latitude: The latitude of the location (EPSG:4326)
        :param longitude: The longitude of the location (EPSG:4326)
        :param hours: Time window of the response in hours
        :return: estimated_actuals
        :raises ValidationError:
            Latitude, longitude or hours are invalid, see response_status for further details
        :raises SiteNotFound: The location is outside our coverage area.
        """
        endpoint = 'estimated_actuals'
        payload = {
            'latitude': latitude,
            'longitude': longitude,
            'hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def _create_uri(self, uri: str, endpoint: str) -> str:
        """Create a URI for specific endpoint."""
        return f'/{uri}/{endpoint}'
