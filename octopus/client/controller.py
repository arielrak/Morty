import json
from flask import Blueprint, abort, jsonify, request

# needed to import config file
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from library.oc_config.oc_config import blacklisted

client = Blueprint('octopus', __name__)
_client_service = None

standard_token = 'KjNksTbCgszxnx3Vubr7'
admin_token = 'EeeIyfb7PEM3uVyKGzzi'

def init_client(client_service):
    global _client_service
    _client_service = client_service

@client.route('/artifacts', methods=['GET'])
def get_artifacts():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    task_id = request.values.get('task_id')
    response = _client_service.get_artifacts(task_id)
    return jsonify(response)

@client.route('/templates', methods=['GET'])
def get_template():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    template_id = request.values.get('id')
    name = request.values.get('name')
    response = _client_service.get_template(template_id, name)
    return jsonify(response)

@client.route('/tasks', methods=['POST'])
def make_request():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    template_id = request.values.get('id')
    name = request.values.get('name')
    parameters = json.loads(request.values.get('parameters'))
    machines = json.loads(request.values.get('machines'))
    _verify_admin_if_needed(name, parameters, request.headers.get('ADMIN_TOKEN'))
    response = _client_service.make_request(name, template_id, parameters, machines)
    return jsonify(response)

@client.route('/tasks', methods=['GET'])
def get_tasks():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    limit = request.values.get('limit')
    response = _client_service.get_tasks(limit)
    return jsonify(response)

@client.route('/task_info', methods=['GET'])
def get_task():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    task_id = request.values.get('id')
    response = _client_service.get_task(task_id)
    return jsonify(response)

@client.route('/names', methods=['GET'])
def get_names():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    response = _client_service.get_names()
    return jsonify(response)

@client.route('/machines', methods=['GET'])
def get_machines():
    _authenticate(request.headers.get('STANDARD_TOKEN'))
    response = _client_service.get_machines()
    return jsonify(response)

def _authenticate(token):
    if token != standard_token:
        abort(403, 'Invalid authentication token.')

def _verify_admin_if_needed(name, parameters, token):
    if admin_needed(name, parameters):
        _authenticate_admin(token)

def admin_needed(name, parameters):
    return name in blacklisted

def _authenticate_admin(token):
    if token != admin_token:
        abort(403, 'You must have permission to run a blacklisted template.')

@client.errorhandler(403)
def custom403(error):
    response = jsonify({'message': error.description})
    return response