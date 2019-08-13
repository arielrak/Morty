import requests
import json

class OctopusInterface:


    def __init__(self, plugin, base_url, standard_token, admin_token):
        self.plugin = plugin
        self.base_url = base_url
        self.standard_token = standard_token
        self.admin_token = admin_token

    def post_request(self, msg, name, template_id, parameters, machines):
        response = requests.post(
            self.base_url + '/tasks',
            headers = self._get_headers(msg),
            data = self._get_parameters(name=name, id=template_id, parameters=parameters, machines=machines)
        )
        return response.json()

    def get_tasks(self, msg, limit):
        response = requests.get(
            self.base_url + '/tasks',
            headers = self._get_headers(msg),
            params = self._get_parameters(limit=limit)
        )
        return response.json()

    def get_task(self, msg, task_id):
        response = requests.get(
            self.base_url + '/task_info',
            headers = self._get_headers(msg),
            params = self._get_parameters(id=task_id)
        )
        return response.json()

    def get_template(self, msg, template_id=None, name=None):
        response = requests.get(
            self.base_url + '/templates',
            headers=self._get_headers(msg),
            params=self._get_parameters(id=template_id, name=name)
        )
        return response.json()

    def get_names(self, msg):
        response = requests.get(
            self.base_url + '/names',
            headers = self._get_headers(msg)
        )
        return response.json()

    def get_artifacts(self, msg, task_id):
        response = requests.get(
            self.base_url + '/artifacts',
            headers = self._get_headers(msg),
            params = self._get_parameters(task_id=task_id)
        )
        return json.loads(response.json())

    def get_machines(self, msg):
        response = requests.get(
            self.base_url + '/machines',
            headers = self._get_headers(msg)
        )
        return response.json()

    def _get_headers(self, msg):
        headers = {'STANDARD_TOKEN': self.standard_token}
        username = msg.frm.username
        if self._is_admin(username):
            headers['ADMIN_TOKEN'] = self.admin_token
        return headers

    def _is_admin(self, username):
        return username in self.plugin['admins']

    def _get_parameters(self, **kwargs):
        parameters = {}
        for argument in kwargs:
            if kwargs[argument] is not None:
                value = kwargs[argument]
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                parameters[argument] = value
        return parameters