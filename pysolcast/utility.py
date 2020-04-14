"""Utility Site Module."""
from pysolcast.base import PySolcast


class UtilitySite(PySolcast):
    """Class for interacting with utility sites.

    Refer to https://docs.solcast.com.au/#utility-scale-sites for more information.
    """

    base_uri = 'utility_scale_sites'

    def get_forecasts(self, period: str, hours: str) -> dict:
        """Get forecasts data for site.

        :param period: Length of the averaging period in ISO8601 duration format.
        :param hours: An offset to which the number of forecasts will be included in the response.
        :return: forecasts
        :raises SiteError:
        """
        endpoint = 'forecasts'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def get_estimated_actuals(self, period: str, hours: str) -> dict:
        """Get estimated actuals data for site.

        :param period: Length of the averaging period in ISO8601 duration format.
        :param hours: An offset to which the number of forecasts will be included in the response.
        :return: estimated_actuals
        :raises SiteError:
        """
        endpoint = 'estimated_actuals'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def get_radiation_forecasts(self, period: str, hours: str) -> dict:
        """Get radiation forecasts data for site.

        :param period: Length of the averaging period in ISO8601 duration format.
        :param hours: An offset to which the number of forecasts will be included in the response.
        :return: forecasts
        :raises SiteError:
        """
        endpoint = 'weather/forecasts'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def get_radiation_estimated_actuals(self, period: str, hours: str) -> dict:
        """Get radiation estimated actual data for site.

        :param period: Length of the averaging period in ISO8601 duration format.
        :param hours: An offset to which the number of forecasts will be included in the response.
        :return: estimated_actuals
        :raises SiteError:
        """
        endpoint = 'weather/estimated_actuals'
        payload = {
            'Period': period,
            'Hours': hours
        }
        return self._get_data(self._create_uri(self.base_uri, endpoint), params=payload)

    def post_measurements(self, data: dict) -> dict:
        """Post measurement data for site.

        :param data: measurement or measurements
        :return: data: data submitted
        :raises ValidationError:
        :raises SiteError:
        """
        endpoint = 'measurements'
        return self._post_data(self._create_uri(self.base_uri, endpoint), data)
