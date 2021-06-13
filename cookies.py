import json
import os


def get_cookies(index, name):
    fp = f'.{name}.cookie'
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()
            data = json.loads(content)
            if isinstance(data, list):
                if len(data) <= index + 1:
                    return data[index]
                else:
                    return {}
            else:
                return data
    return {}


def save_cookies(index, name, cookies):
    data = []
    fp = f'.{name}.cookie'
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()
            if content:
                data = json.loads(content)
                if isinstance(data, dict):
                    data = [data]

    if len(data) < index + 1:
        for _ in range(index + 1 - len(data)):
            data.append({})

    with open(fp, 'w') as f:
        data[index] = cookies
        f.write(json.dumps(data))
