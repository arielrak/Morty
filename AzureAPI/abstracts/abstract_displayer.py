from abc import ABC, abstractmethod
from json.decoder import JSONObject


class AbstractDisplayer(ABC):

    @abstractmethod
    def make_table(self, json: JSONObject, image_url: str) -> None:
        pass