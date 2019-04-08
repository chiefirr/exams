import os

import funcy

from additional_tasks.helpers import parse_file_content_json
from exams.settings import BASE_DIR

FILENAME = 'accounting_input.txt'
FILEPATH = os.path.join(BASE_DIR, 'additional_tasks', 'files', FILENAME)


def accounting():
    ctr = 0

    def count(content):
        nonlocal ctr
        for item in funcy.flatten(content):
            if isinstance(item, int):
                ctr += item
            elif isinstance(item, dict):
                count(item.values())
        return ctr

    return count


if __name__ == '__main__':
    content = parse_file_content_json(FILEPATH)
    counter = accounting()
    result = counter(content.values())
    print("Result is: ", result)
