from octopus_client import OctopusClient
from app import OctopusApiServer
from client_config import base_url, api_key

client = OctopusClient(
    base_url=base_url,
    api_key=api_key
)

api_server = OctopusApiServer(client)
api_server.run()