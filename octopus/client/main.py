from octopus_client import OctopusClient
from app import OctopusApiServer

client = OctopusClient(
    base_url='https://chatops.octopus.app/api',
    api_key='API-5G9QUKBMCRMVNPQRUN7BEIOYOI0'
    #api_key='API-SWNWJ53CQEDJGXMZRDRDL1JKLA'
)

api_server = OctopusApiServer(client)
api_server.run()