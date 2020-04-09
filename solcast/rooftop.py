"""Rooftop Site Module."""
from solcast.base import Solcast, parse_date_time


class RooftopSite(Solcast):
    """Class for interacting with Rooftop sites.

    Refer to https://docs.solcast.com.au/#rooftop-sites for more information.
    """

    base_uri = 'rooftop_sites'

    def get_forecasts(self) -> dict:
        """Get forecasts data for site.

        :return: forecasts:
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'forecasts'
        return self._get_data(self._create_uri(self.base_uri, endpoint))

    def get_forecasts_parsed(self) -> dict:
        """Get forecasts data for site.

        :return: forecasts: Date is parsed as a datetime object.
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'forecasts'
        forecasts = self._get_data(self._create_uri(self.base_uri, endpoint))
        return parse_date_time(forecasts, endpoint)

    def get_estimated_actuals(self) -> dict:
        """Get estimated actuals data for site.

        :return: estimated_actuals:
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'estimated_actuals'
        return self._get_data(self._create_uri(self.base_uri, endpoint))

    def post_measurements(self, data: dict) -> dict:
        """Post measurement data for site.

        :param data: measurement or measurements
        :return: data: Returns data submitted
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'measurements'
        return self._post_data(self._create_uri(self.base_uri, endpoint), data)
