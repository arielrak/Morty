Blacklisted templates and templates that should be ignored by default when fetching a list of template names are set in:
	/path/to/errbot-root/plugins/octopus/library/oc_config/oc_config.py

Predefined parameter settings are also set there.
The structure of the predefined variable is a nested dictionary with the following structure:
predefined = {
	NAME_OF_TEMPLATE: {
		NAME_OF_PARAMETER_SETTING: {
			PARAMETER_1: VALUE_1,
			PARAMETER_2: VALUE_2
}

This plugin requires a client server connected to Octopus Deploy to be running.
This server can be run through:
	python3 /path/to/errbot-root/plugins/octopus/client/main.py &

Some configurations for the client server are set in the file /path/to/errbot-root/plugins/octopus/client/client_config.py
The file should be included in your .gitignore
The variables and their sample values are listed below.

base_url: url of Octopus Deploy instance ('https://chatops.octopus.app/api')
api_key= api key of Octopus Deploy instance ('API-5G9QUKBMCRMVNPQRUN7BEIOYOI0')

host: hostname that the client server will run on ('127.0.0.1')
port: port of the client server (5000)
client_url: the url that will be accessed to send requests to the client server

standard_token: tokens that must be sent to authenticate requests to the client server ('KjNksTbCgszxnx3Vubr7')
admin_token: admins must send both the standard token and the admin token to access admin-only functions ('EeeIyfb7PEM3uVyKGzzi')
Tokens are sent in the header of requests, under STANDARD_TOKEN and ADMIN_TOKEN respectively.