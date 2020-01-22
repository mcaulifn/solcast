"""Main module."""
from dataclasses import dataclass, asdict
from datetime import datetime
import requests
from solcast.base import Solcast


class RooftopSite(Solcast):

    base_uri = '/rooftop_sites/'

    def __init__(self, api_key, resource_id):
        super().__init__(api_key, resource_id)

    def get_forecasts(self):
        endpoint = '/forecasts'
        return self._get_data(self.create_uri(self.base_uri, endpoint))

    def get_estimated_actuals(self):
        endpoint = '/estimated_actuals'
        return self._get_data(self.create_uri(self.base_uri, endpoint))

    def post_measurements(self, data: dict):
        endpoint = '/measurements'
        return self._post_data(self.create_uri(self.base_uri, endpoint), data)


@dataclass
class Forecast:
    """"""
    pv_estimate: str
    pv_estimate10: str
    pv_estimate90: str
    period_end: str  # = "2018-01-01T01:00:00.00000Z"
    period: str  # = "PT30M"


@dataclass
class EstimatedActuals:
    """"""
    pv_estimate: str
    period_end: str
    period: str
