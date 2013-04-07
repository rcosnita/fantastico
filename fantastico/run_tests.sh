#!/bin/sh
nosetests-3.2 --all-modules --with-xcoverage --cover-erase --cover-tests --cover-package=fantastico --xcoverage-file=fantastico_coverage.xml --with-xunit --xunit-file=fantastico_tests.xml -v