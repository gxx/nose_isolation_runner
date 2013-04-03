#!/usr/bin/python
# coding=utf-8
"""Run nose tests in proper isolation and collect coverage reports"""
import os
import subprocess
import sys

from find import find


COVER_OPTION = '--with-cover'
COVERAGE_FILE = '.coverage'
FAIL_MESSAGE = ' [FAILED!]\n'
ERROR_MESSAGE = ' [ERROR!]\n'
OK_MESSAGE = ' [OK]\n'


def run(directory='.', *options):
    """Runs nose tests in isolation, and aggregates the coverage reports
    :param directory: directory in which to run the nose tests
    """
    options = list(options)
    if COVER_OPTION in options:
        options.remove(COVER_OPTION)

    current_working_directory = os.getcwd()
    found_tests = [test for test in find(directory)]
    succeeded = 0
    if found_tests:
        print 'Found %d tests' % len(found_tests)
        for number, test in enumerate(found_tests):
            test_number = number + 1
            sys.stdout.write('Running test #%d...' % test_number)
            sys.stdout.flush()
            process = subprocess.Popen(['nosetests', test, COVER_OPTION] + options,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if process.wait():
                sys.stdout.write(FAIL_MESSAGE)
                sys.stdout.write('Test failed: "%s"\n'
                                 % os.path.relpath(test, current_working_directory))
                sys.stdout.flush()
            else:
                sys.stdout.write(OK_MESSAGE)
                sys.stdout.flush()
                if os.path.exists(COVERAGE_FILE):
                    os.rename(COVERAGE_FILE, '.coverage.%d' % test_number)
                    succeeded += 1
                else:
                    sys.stdout.write(ERROR_MESSAGE)
                    sys.stdout.flush()
                    sys.stderr.write('Cannot find coverage file\n')
                    sys.stderr.flush()

        sys.stdout.write('%d of %d tests passed\n' % (succeeded, len(found_tests)))
        sys.stdout.write('Combining coverage data...')
        sys.stdout.flush()
        process = subprocess.Popen(['coverage', 'combine'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        if process.wait():
            sys.stdout.write(ERROR_MESSAGE)
            sys.stdout.flush()
            sys.stderr.write(process.stderr.read())
            sys.stderr.flush()
            sys.exit(1)
        else:
            sys.stdout.write(OK_MESSAGE)
            sys.stdout.flush()
    else:
        print 'Did not find any tests to run'


def main():
    if len(sys.argv) > 1:
        run(*sys.argv[1:])
    else:
        run()

if __name__ == '__main__':
    main()
