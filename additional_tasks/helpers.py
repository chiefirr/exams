import json


def parse_file_content(filepath):
    with open(filepath, 'r') as input:
        content = input.read().splitlines()
    return content


def parse_file_content_json(filepath):
    with open(filepath, 'r') as input:
        content = json.load(input)
    return content
