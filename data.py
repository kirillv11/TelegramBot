import json
from random import randint

with open("data.json") as f:
    file_content = f.read()
    templates = json.loads(file_content)
    length = len(templates['image'])
    print(templates['image'][randint(0, length - 1)]['path'])