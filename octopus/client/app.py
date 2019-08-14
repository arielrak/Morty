from flask import Flask

from controller import client, init_client
from client_config import host, port

class OctopusApiServer:
    def __init__(self, client_service):
        self._client_service = client_service
        self._app = Flask(__name__)
        self._init_routes()

    def _init_routes(self):
        self._app.register_blueprint(client, url_prefix='/octopus')
        init_client(self._client_service)

    def run(self):
        self._app.run(host=host, port=port)