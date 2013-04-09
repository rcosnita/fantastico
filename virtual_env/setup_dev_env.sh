#!/bin/sh
PATH=/usr/bin:/usr/local/bin:/usr/sbin

virtualenv-3.2 --distribute pip-deps

source pip-deps/bin/activate
pip-3.2 install nose
pip-3.2 install pylint
pip-3.2 install jinja2
pip-3.2 install sphinx