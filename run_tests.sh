#!/bin/bash

. pip-deps/bin/activate

find fantastico -regextype sed -regex '.*/test_.*\.py' | xargs nosetests-3.2 --with-coverage --cover-erase --cover-tests --cover-package=fantastico --cover-xml --with-xunit --xunit-file=fantastico_tests.xml -v