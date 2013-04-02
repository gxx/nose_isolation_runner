#!/usr/bin/python
# coding=utf-8
"""Run nose tests in proper isolation and collect coverage reports"""
import os
import subprocess
import sys

from find import find


def run(directory='.'):
    """Runs nose tests in isolation, and aggregates the coverage reports
    :param directory: directory in which to run the nose tests
    """
    found_tests = [test for test in find(directory)]
    succeeded = []
    if found_tests:
        print 'Found %d tests' % len(found_tests)
        for number, test in enumerate(found_tests):
            test_number = number + 1
            sys.stdout.write('Running test #%d...' % test_number)
            sys.stdout.flush()
            process = subprocess.Popen(['nosetests', test, '--with-cover'],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if process.wait():
                sys.stdout.write(' [FAILED!]\n')
                sys.stdout.flush()
            else:
                sys.stdout.write(' [OK]\n')
                sys.stdout.flush()
                if os.path.exists('.coverage'):
                    os.rename('.coverage', '.coverage.%d' % test_number)
                    succeeded.append(test_number)
                else:
                    sys.stdout.write(' [ERROR!]\n')
                    sys.stdout.flush()
                    sys.stderr.write('Cannot find coverage file\n')
                    sys.stderr.flush()

        sys.stdout.write('Combining coverage data...')
        process = subprocess.Popen(['coverage', 'combine'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        if process.wait():
            sys.stdout.write(' [ERROR!]\n')
            sys.stdout.flush()
            sys.stderr.write(process.stderr.read())
            sys.stderr.flush()
            sys.exit(1)
        else:
            sys.stdout.write(' [OK]\n')
            sys.stdout.flush()
    else:
        print 'Did not find any tests to run'


def main():
    if len(sys.argv) > 2:
        sys.stderr.write('Too many arguments provided for directory\n')
        sys.stderr.flush()
        sys.exit(1)
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        run()

if __name__ == '__main__':
    main()
