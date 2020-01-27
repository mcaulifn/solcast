"""Weather site module."""
from solcast.base import Solcast


class WeatherSite(Solcast):
    """Class for interacting with weather sites."""

    base_uri = 'weather_sites'

    def get_forecasts(self) -> dict:
        """Get forecasts data for site."""
        endpoint = 'forecasts'
        return self._get_data(self.create_uri(self.base_uri, endpoint))

    def get_estimated_actuals(self) -> dict:
        """Get estimated actuals data for site."""
        endpoint = 'estimated_actuals'
        return self._get_data(self.create_uri(self.base_uri, endpoint))
