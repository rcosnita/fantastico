#!/bin/bash
PATH=/bin:/usr/bin:/usr/sbin

if [[ -z $ROOT_PASSWD ]]; then
	echo "You must set ROOT_PASSWD environment variable before setting up prod environment."
	
	exit 1
fi

ALL_ARGS=$@
VHOST_NAME=""

set -- $(getopt -l ipaddress,vhost-name,http-port,uwsgi-port,root-folder,modules-folder: -- "$@")
while [ $# -gt 0 ]
do
    case "$1" in
    	(--vhost-name) VHOST_NAME=$2;;
    esac
    shift
done

if [[ -z $VHOST_NAME ]]; then
	echo "You must provide VHOST_NAME"
	
	exit 1
fi

VHOST_NAME=`echo $VHOST_NAME | sed -s "s/^\(\(\"\(.*\)\"\)\|\('\(.*\)'\)\)\$/\\3\\5/g"`
NGINX_CONF=$VHOST_NAME.conf

echo $ROOT_PASSWD | sudo -S apt-get install nginx -y

. pip-deps/bin/activate

export PYTHONPATH=`pwd`

echo "Generating nginx conf file $NGINX_CONF"

python3 fantastico/deployment/config_nginx.py $ALL_ARGS >> $NGINX_CONF

if [ $? -gt 0 ]; then
	exit $?
fi

echo $ROOT_PASSWD | sudo -S mv $NGINX_CONF /etc/nginx/sites-available/$NGINX_CONF
echo $ROOT_PASSWD | sudo -S ln -fs /etc/nginx/sites-available/$NGINX_CONF /etc/nginx/sites-enabled/$NGINX_CONF
echo $ROOT_PASSWD | sudo -S service nginx restart

# config s3fs
# python3 fantastico/deployment/config_s3.py /etc