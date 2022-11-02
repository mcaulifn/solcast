"""Rooftop Site Module."""
from pysolcast.base import PySolcast, parse_date_time


class RooftopSite(PySolcast):
    """Class for interacting with Legacy Rooftop sites.

    Refer to https://docs.solcast.com.au/#58ca9bc0-27d4-4418-937f-03986331f01d for more information.
    """

    base_uri = 'rooftop_sites'

    def get_forecasts(self, params: dict = None) -> dict:
        """Get forecasts data for site.

        :return: forecasts:
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'forecasts'
        return self._get_data(self._create_uri(self.base_uri, endpoint), params)

    def get_forecasts_parsed(self, params: dict = None) -> dict:
        """Get forecasts data for site.

        :return: forecasts: Date is parsed as a datetime object.
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'forecasts'
        forecasts = self._get_data(self._create_uri(self.base_uri, endpoint), params)
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
