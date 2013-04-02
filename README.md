nose_isolation_runner
=====================

An isolation runner for nose to handle some badly written tests causing test environment pollution to be propagated between test cases.

Usage:

## isolation.py
isolation.py [subdirectory or nothing for current working directory]

isolation.py will run all tests under the subdirectory/cwd and aggregate the coverage reports for you, in completely separate nosetest instances to prevent any chance of testcase pollution.

## find.py
find.py [subdirector(y/ies) or nothing for current working directory]

find.py will find and print out all tests using the regex ```(^|[b_./-])[Tt]est.*.py(?<!=__init__\.py)$```, which is basically the same as the nose regex, with the addition of checking if it's a python file and that it's not the ```__init__.py``` file within the regex.
