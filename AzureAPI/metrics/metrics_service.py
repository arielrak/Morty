import json
from typing import Iterable

from abstracts.abstract_api_interface import AbstractAPIInterface


class MetricsService:

    def __init__(self, api_interface: AbstractAPIInterface):
        self._api_interface = api_interface

    def get_all_metrics(self) -> Iterable[str]:
        raw_json = self._api_interface.make_get_request("metrics", "metadata")

        if raw_json["metrics"] is not None:
            return raw_json["metrics"]
        else:
            return None


    def get_metric(self, args_provided: dict) -> dict:
        if args_provided.metric_id is None:
            return "Please provide a metric ID"

        args_copy_without_metricid = vars(args_provided).copy()
        args_copy_without_metricid.pop('metric_id', None)

        raw_json = self._api_interface.make_get_request("metrics", args_provided.metric_id, args_copy_without_metricid)

        return raw_json