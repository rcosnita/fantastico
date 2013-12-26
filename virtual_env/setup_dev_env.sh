#!/bin/bash
PATH=/bin:/usr/bin:/usr/local/bin:/usr/sbin

. pip-deps/bin/activate
pip install nose
pip install coverage
pip install pylint
pip install jinja2==2.6
pip install sphinx
pip install webob
pip install virtual_env/libs/mysql-connector
pip install sqlalchemy
pip install mock
pip install uwsgi
pip install "pycrypto>=2.6"
