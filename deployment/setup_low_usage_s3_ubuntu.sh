#!/bin/bash
PATH=/usr/bin:/usr/sbin

sudo apt-get install nginx -y

. ../pip-deps/bin/activate
# python3 fantastico/deployment/config_nginx.py /etc/nginx

# config s3fs
# python3 fantastico/deploymnet/config_s3.py /etc