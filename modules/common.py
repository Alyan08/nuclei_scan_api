import yaml
import ipaddress
from flask import request, make_response, jsonify
from functools import wraps


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    from_ip = ipaddress.ip_address(config['ip_range']['from_ip'])
    to_ip = ipaddress.ip_address(config['ip_range']['to_ip'])
    api_key = config['x-api-key']


def source_ip_allowed():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = ipaddress.ip_address(request.remote_addr)
            if from_ip <= client_ip <= to_ip:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Forbidden"}), 403
        return wrapper
    return decorator


def check_api_key():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x_api_key = request.headers.get('X-API-KEY')
            if x_api_key == api_key:
                return func(*args, **kwargs)
            else:
                return make_response(jsonify({"status": False, "reason": "wrong x-apy-key"}), 403)
        return wrapper
    return decorator


def scan_params_sent():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            target = request.args.get('target')
            severity = request.args.get('severity')

            if target and severity in ["critical", "high", "medium", "low", "info"]:
                return func(*args, **kwargs)
            else:
                return make_response(jsonify({"status": False, "reason": "please check params!"}), 400)
        return wrapper
    return decorator