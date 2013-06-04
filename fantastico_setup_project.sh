#!/bin/bash

if [ -z "$1" ]; then
	echo "You must provide python folder from pip library. E.g: python3.2"
	exit
fi;

if [ -z "$2" ]; then
	echo "You must provide your project name. E.g my-project"
	exit
fi;

PYTHON_LIB_FOLDER=$1
PROJECT_NAME=$2

PATH=/bin:/usr/bin:/usr/sbin

echo "Adding Fantastico virtual_env scripts to root folder."
ln -sf pip-deps/scripts/fantastico/virtual_env .
chmod u+x virtual_env/setup_dev_env.sh
./virtual_env/setup_dev_env.sh

cd pip-deps/bin

echo 'Adding Fantastico scripts to path.'

ln -sf ../scripts/fantastico/run_dev_server.sh fantastico_run_dev_server
chmod u+x fantastico_run_dev_server

ln -sf ../scripts/fantastico/run_prod_server.sh fantastico_run_prod_server
chmod u+x fantastico_run_prod_server

ln -sf ../scripts/fantastico/deployment/setup_low_usage_ubuntu.sh fantastico_setup_low_usage_ubuntu
chmod u+x fantastico_setup_low_usage_ubuntu

ln -sf ../scripts/fantastico/deployment/setup_low_usage_s3_ubuntu.sh fantastico_setup_low_usage_s3_ubuntu
chmod u+x fantastico_setup_low_usage_s3_ubuntu

cd ../../

echo "Linking fantastico minimum deps."
ln -sf pip-deps/lib/$PYTHON_LIB_FOLDER/site-packages/fantastico .

if [ ! -d deployment ]; then
	mkdir deployment
	cp -R pip-deps/scripts/fantastico/deployment/conf deployment/
fi

if [ ! -d $PROJECT_NAME ]; then
	cp -R pip-deps/scripts/fantastico/project_template/project $PROJECT_NAME
fi