#!/bin/bash

. ../pip-deps/bin/activate

pylint -f parseable --max-line-length=130 . | tee pylint.out