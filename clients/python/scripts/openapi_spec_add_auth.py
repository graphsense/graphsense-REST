import yaml
import sys
import os
import json

input_filename = sys.argv[1]
rest_url = sys.argv[2] if len(sys.argv) > 2 else ""
dirname = os.path.dirname(input_filename)
stats_path = '/stats'

security_schemes = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

with open(input_filename, 'r') as input_file:
    input = yaml.safe_load(input_file)
    if rest_url:
        input['servers'][0]['url'] = rest_url

    if 'components' not in input:
        input['components'] = {}
    if 'securitySchemes' not in input['components']:
        input['components']['securitySchemes'] = {}

    input['components']['securitySchemes'] = security_schemes
    input['security'] = [{'cookieAuth': []}]

    for path in input['paths']:
        path_yaml = input['paths'][path]
        for operation in path_yaml:
            if path == stats_path and operation == 'get':
                path_yaml[operation]['security'] = []
            else:
                path_yaml[operation]['security'] = \
                    [{'api_key': []}]

    print(json.dumps(input))

    input_file.close()
