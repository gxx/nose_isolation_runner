nose_isolation_runner
=====================

An isolation runner for nose to handle some badly written tests causing test environment pollution to be propagated between test cases.

#Usage:

## isolation.py
isolation.py [subdirectory or nothing for current working directory]

isolation.py will run all tests under the subdirectory/cwd and aggregate the coverage reports for you, in completely separate nosetest instances to prevent any chance of testcase pollution.

## find.py
find.py [subdirector(y/ies) or nothing for current working directory]

find.py will find and print out all tests using the regex ```(?:^|[b_./-])(?:[Tt]est|[Ss]pec).*.py(?<!__init__\.py)```, which is basically the same as the nose regex, with the addition of checking if it's a python file and that it's not the ```__init__.py``` file within the regex and matching files with spec instead of test.

# Example run:

```
Found 12 tests
Running test #1... [OK]
Running test #2... [OK]
Running test #3... [OK]
Running test #4... [OK]
Running test #5... [OK]
Running test #6... [OK]
Running test #7... [OK]
Running test #8... [OK]
Running test #9... [OK]
Running test #10... [OK]
Running test #11... [OK]
Running test #12... [OK]
12 of 12 tests passed
Combining coverage data... [OK]
```
