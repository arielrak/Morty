from html import unescape
from urllib.parse import quote
from json.decoder import JSONObject

import requests

from abstracts.abstract_api_interface import AbstractAPIInterface


class RequestExecutor(AbstractAPIInterface):

    def __init__(self, app_id, app_key, slack_key):
        self._app_id = app_id
        self._app_key = app_key
        self._slack_key = slack_key

    # General purpose method for making get requests
    def make_get_request(self, type: str, id: str, options: dict = None) -> JSONObject:
        url = self._generate_base_url(type, id)
        url = self._append_options_to_url(url, options)
        print("Sending GET request to "+url)

        header = {"x-api-key": self._app_key}

        request = requests.get(url, headers=header)
        if request.headers.get('content-type').find('json') != -1:
            return request.json()
        else:
            return request.text

    def _generate_base_url(self, type: str, id: str):
        url = "https://api.applicationinsights.io/v1/apps/" + self._app_id + "/" + type

        if id is not None:
            url += "/" + id + "?"
        else:
            url += "?"

        return url

    def _append_options_to_url(self, url:str, options: dict):
        if options is not None:
            for key, value in options.items():
                if value is not None:
                    value = unescape(value)
                    url += key + "=" + quote(value) + "&"
        return url

    def send_image(self, file_url: str, channel: str):
        url = "https://slack.com/api/files.upload"
        header = {"Authorization": "Bearer "+self._slack_key}
        files = {"channels":(None,channel),
                 "file":(file_url, open(file_url, 'rb'))}

        request = requests.put(url, headers=header, files=files)