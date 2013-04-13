#!/bin/bash

. ../pip-deps/bin/activate

nosetests-3.2 --all-modules --with-coverage --cover-erase --cover-tests --cover-package=fantastico --with-xunit --xunit-file=fantastico_tests.xml -v
coverage xml