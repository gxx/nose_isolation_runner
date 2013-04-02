#!/usr/bin/python
# coding=utf-8
"""Find nose tests"""
import os
import re
import sys


TEST_MATCHER = re.compile(r'(^|[b_./-])[Tt]est.*.py(?<!=__init__\.py)$')


def find(path='./'):

    for root_directory, _, file_names in os.walk(path):
        for file_name in file_names:
            if TEST_MATCHER.search(file_name):
                yield os.path.join(root_directory, file_name)


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
