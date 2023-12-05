import json
import os

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema')


def load_schema(filepath):
    with open(os.path.join(SCHEMA_PATH, filepath)) as file:
        schema = json.load(file)
        return schema
