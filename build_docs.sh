#!/bin/sh
export PYTHONPATH=`pwd`
cd doc
make clean html epub latexpdf
