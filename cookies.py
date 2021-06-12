import json
import os


def get_cookies(name):
    fp = f'.{name}.cookie'
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()
            return json.loads(content)
    return {}

def save_cookies(name, cookies):
    with open(f'.{name}.cookie', 'w') as f:
        f.write(json.dumps(cookies))
