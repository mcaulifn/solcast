"""Main module."""
from solcast.base import Solcast


class UtilitySite(Solcast):
    """Class for interacting with utility sites."""

    base_uri = 'utility_scale_sites'

    def get_forecasts(self, period, hours):
        """Get forecasts data for site."""
        endpoint = 'forecasts'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def get_estimated_actuals(self, period, hours):
        """Get estimated actuals data for site."""
        endpoint = 'estimated_actuals'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def get_radiation_forecasts(self, period, hours):
        """Get radiation forecasts data for site."""
        endpoint = 'weather/forecasts'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def get_radiation_estimated_actuals(self, period, hours):
        """Get radiation estimated actual data for site."""
        endpoint = 'weather/estimated_actuals'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self.create_uri(self.base_uri, endpoint), params=payload)

    def post_measurements(self, data: dict):
        """Post measurement data for site."""
        endpoint = 'measurements'
        return self._post_data(self.create_uri(self.base_uri, endpoint), data)
