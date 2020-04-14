"""Weather site Module."""
from pysolcast.base import PySolcast


class WeatherSite(PySolcast):
    """Class for interacting with weather sites.

    Refer to https://docs.solcast.com.au/#weather-site for more information.
    """

    base_uri = 'weather_sites'

    def get_forecasts(self) -> dict:
        """Get forecasts data for site.

        :returns: forecasts
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'forecasts'
        return self._get_data(self._create_uri(self.base_uri, endpoint))

    def get_estimated_actuals(self) -> dict:
        """Get estimated actuals data for site.

        :returns: estimated_actuals
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'estimated_actuals'
        return self._get_data(self._create_uri(self.base_uri, endpoint))
