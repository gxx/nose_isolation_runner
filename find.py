#!/usr/bin/python
# coding=utf-8
"""Find nose tests"""
import fnmatch
import os
import re
import sys


TEST_MATCHER = re.compile(r'(?:^|[b_./-])(?:[Tt]est|[Ss]pec).*\.py(?<!__init__\.py)$')
RELATIVE_PATHS = set(('.', '..'))


class GitIgnoreMatcher(object):
    def __init__(self, *patterns):
        self.patterns = patterns

    @staticmethod
    def load(path):
        with open(path, 'r') as ignore_file:
            raw_contents = ignore_file.read()
            sane_contents = filter(None, raw_contents.split('\n'))
            return GitIgnoreMatcher(*sane_contents)

    def match(self, path):
        return any(fnmatch.fnmatchcase(path, pattern) for pattern in self.patterns)


def no_hidden_path(path):
    """Find out whether a portion of the file path is hidden
    :param path: The file path to evaluation
    :return: True if the file path isn't hidden in any part, False otherwise
    """
    head, tail = os.path.split(path)
    if tail.startswith('.') and tail not in RELATIVE_PATHS:
        return False

    if head:
        return no_hidden_path(head)
    else:
        return True


def find(path='./'):
    """Find tests within the given path
    :param path: The path in which to find tests
    """
    try:
        ignore_matcher = GitIgnoreMatcher.load(os.path.join(path, '.gitignore'))
    except IOError:
        ignore_matcher = GitIgnoreMatcher() # Dummy empty matcher

    for root_directory, _, file_names in os.walk(path):
        for file_name in file_names:
            full_path = os.path.join(root_directory, file_name)
            if (TEST_MATCHER.search(full_path) and no_hidden_path(full_path)
                    and not ignore_matcher.match(full_path)):
                yield full_path


def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            for found in find(arg):
                print found
    else:
        for found in find():
            print found


if __name__ == '__main__':
    main()
