#!/bin/bash
. ./pip-deps/bin/activate

echo "Building Fantastico $FANTASTICO_VERSION version."

export PYTHONPATH=`pwd`
cd doc
make clean html epub latexpdf