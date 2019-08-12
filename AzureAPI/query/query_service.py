import json
import os

from abstracts.abstract_api_interface import AbstractAPIInterface

class QueryService:

    def __init__(self, api_interface: AbstractAPIInterface):
        self._api_interface = api_interface

    def get_preset_query(self, query_name):
        if query_name in self._get_presets_dict():
            query = self._get_presets_dict()[query_name]
        else:
            return None

        return self._api_interface.make_get_request("query", None, {"query": query})

    def get_custom_query(self, query):

        return self._api_interface.make_get_request("query", None, {"query": query})

    def get_all_presets_as_list(self):
        return [key+" ("+value+")" for key, value in self._get_presets_dict().items()]

    def add_preset(self, query: str, name: str):
        presets = self._get_presets_dict()
        presets.update({name: query})
        self._write_new_presets_dict(presets)

    def _get_presets_dict(self):
        if not os.path.isfile("plugins/AzureAPI/query/query_presets.json"):
            return {}
        with open("plugins/AzureAPI/query/query_presets.json", "r") as file:
            return json.load(file)

    def _write_new_presets_dict(self, new_dict: dict):
        with open("plugins/AzureAPI/query/query_presets.json", "w") as file:
            file.write(json.dumps(new_dict))