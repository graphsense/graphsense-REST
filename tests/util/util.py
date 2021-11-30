import yaml


def yamldump(data):
    if isinstance(data, list):
        data = [d.to_dict() for d in data]
    else:
        data = data.to_dict()
    print(yaml.dump(data))
