import os

from additional_tasks.helpers import parse_file_content
from exams.settings import BASE_DIR

FILENAME = 'skyphrase_input.txt'
FILEPATH = os.path.join(BASE_DIR, 'additional_tasks', 'files', FILENAME)


def checker_unique(content):
    ctr = 0
    for line in content:
        line_splited = line.split(' ')
        ctr += len(set(line_splited)) == len(line_splited)
    return ctr


if __name__ == '__main__':
    content = parse_file_content(FILEPATH)
    result = checker_unique(content)

    print("Len unique: ", result)
    print("Len content: ", len(content))
