from abc import ABC, abstractmethod
from json.decoder import JSONObject


class AbstractAPIInterface(ABC):

    @abstractmethod
    def make_get_request(self, type: str, id: str, options: dict = None) -> JSONObject:
        pass