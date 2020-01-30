"""Main module."""
from solcast.base import Solcast, parse_date_time


class RooftopSite(Solcast):
    """Class for interacting with Rooftop."""

    base_uri = 'rooftop_sites'

    def get_forecasts(self) -> dict:
        """Get forecasts data for site."""
        endpoint = 'forecasts'
        forecasts = self._get_data(self.create_uri(self.base_uri, endpoint))
        return parse_date_time(forecasts, endpoint)

    def get_estimated_actuals(self) -> dict:
        """Get estimated actuals data for site."""
        endpoint = 'estimated_actuals'
        return self._get_data(self.create_uri(self.base_uri, endpoint))

    def post_measurements(self, data: dict):
        """Post measurement data for site."""
        endpoint = 'measurements'
        return self._post_data(self.create_uri(self.base_uri, endpoint), data)
