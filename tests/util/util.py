import yaml
import json
from openapi_server.encoder import JSONEncoder


def yamldump(obj):
    print(yaml.dump(json.loads(json.dumps(obj, cls=JSONEncoder))))
