#!/bin/bash
PATH=/usr/bin:/usr/sbin

echo loopless | sudo -S apt-get install nginx -y

. ../pip-deps/bin/activate

export PYTHONPATH=`pwd`/../

python3 ../fantastico/deployment/config_nginx.py --ipaddress 127.0.0.1 --vhost-name fantastico-framework.com --uwsgi-port 12090 --root-folder `pwd` --modules-folder /fantastico/samples >> fantastico-framework.com.conf

echo ROOT_PASSWD | sudo -S mv fantastico-framework.com.conf /etc/nginx/sites-available/fantastico-framework.com.conf
echo ROOT_PASSWD | sudo -S ln -fs /etc/nginx/sites-available/fantastico-framework.com.conf /etc/nginx/sites-enabled/fantastico-framework.com.conf
echo ROOT_PASSWD | sudo -S service nginx restart

# config s3fs
# python3 fantastico/deployment/config_s3.py /etc