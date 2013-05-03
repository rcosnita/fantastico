#!/bin/bash

. pip-deps/bin/activate

export PYTHONPATH=`pwd`

python3 fantastico/server/dev_server.py