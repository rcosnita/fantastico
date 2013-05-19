#!/bin/bash

. pip-deps/bin/activate

export PYTHONPATH=`pwd`

uwsgi deployment/conf/nginx/fantastico-uwsgi.ini