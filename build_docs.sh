#!/bin/bash
. ./pip-deps/bin/activate

export PYTHONPATH=`pwd`
cd doc
make clean html epub latexpdf