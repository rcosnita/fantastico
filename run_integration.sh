#!/bin/bash

. pip-deps/bin/activate

find fantastico -regextype sed -not -regex '.*/test_.*\.py' -name '*.py' | xargs nosetests-3.2 --with-coverage --cover-erase --cover-tests --cover-package=fantastico --cover-xml --cover-xml-file=coverage_integration.xml --with-xunit --xunit-file=fantastico_integration_tests.xml -v