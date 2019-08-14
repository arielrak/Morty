import requests
import json
import io

class OctopusClient:
     
    def __init__(self, base_url, api_key):
         self.base_url = base_url
         self.headers = {'X-Octopus-ApiKey': api_key}

    def get_template(self, template_id, name):
        if template_id is not None:
            return self._get_template_by_id(template_id)
        else:
            return self._get_template_by_name(name)

    def _get_template_by_name(self, name):
        template_list = self._get_template_list()
        for template in template_list:
            if template['Name'] == name:
                return template

    def _get_template_by_id(self, template_id):
        template_list = self._get_template_list()
        for template in template_list:
            if template['Id'] == template_id:
                return template

    def make_request(self, name, template_id, parameters, machines):
        body = self._make_body(name, template_id, parameters, machines)
        response = self._post('/tasks', body)
        json_response = response.json()
        return json_response

    def get_names(self):
        template_list = self._get_template_list()
        name_list = []
        for template in template_list:
            name_list.append((
                template['Name'], 
                template['Id'].lstrip('ActionTemplates-')
            ))
        name_list.sort(key=lambda item: int(item[1]))
        return name_list

    def get_machines(self):
        response = self._get('/machines/all')
        return response.json()

    def get_tasks(self, limit=None):
        if limit is None:
            limit = 10
        else:
            limit = int(limit)
        response = self._get('/tasks')
        response_info = response.json()
        task_list = response_info['Items']
        return task_list[:limit]

    def get_task(self, task_id):
        response = self._get('/tasks/' + task_id)
        return response.json()

    def _get(self, route):
        return requests.get(
            self.base_url + route,
            headers = self.headers
        )
    
    def _post(self, route, body):
        return requests.post(
            self.base_url + route,
            headers = self.headers,
            data = json.dumps(body)
        )
    
    def _make_body(self, name, template_id, parameters, machines):
        return {
            "Name": "AdHocScript",
            "Description": "Run step template: " + name,
            "Arguments": {
                "Properties": parameters,
                "ActionTemplateId": template_id,
                "MachineIds": machines
            }
        }

    def get_artifacts(self, task_id):
        artifact_list = self._get_artifact_list(task_id)['Items']
        artifact_info = []
        for artifact in artifact_list:
            artifact_id = artifact['Id']
            artifact_name = artifact['Filename']
            artifact_url = self._get_artifact(artifact_id)
            artifact_info.append([artifact_name, artifact_url])
        return json.dumps(artifact_info)

    def _get_artifact(self, artifact_id):
        return "{}/artifacts/{}/content".format(self.base_url, artifact_id)

    def _get_artifact_list(self, task_id):
        route = "/artifacts?regarding=ServerTasks-" + task_id
        response = self._get(route)
        return response.json()

    def _get_template_list(self):
        response = requests.get(
            self.base_url + "/actiontemplates",
            headers = self.headers
        )
        response_info = response.json()
        template_list = response_info['Items']
        return template_list