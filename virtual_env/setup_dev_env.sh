#!/bin/bash
PATH=/usr/bin:/usr/local/bin:/usr/sbin

virtualenv-3.2 --distribute pip-deps

. pip-deps/bin/activate
pip-3.2 install nose
pip-3.2 install coverage
pip-3.2 install pylint
pip-3.2 install jinja2==2.6
pip-3.2 install sphinx
pip-3.2 install webob
pip-3.2 install virtual_env/libs/mysql-connector
pip-3.2 install sqlalchemy
pip-3.2 install mock
pip-3.2 install uwsgi
pip-3.2 install "pycrypto>=2.6"
