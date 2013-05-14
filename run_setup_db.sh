#!/bin/bash

. pip-deps/bin/activate

/usr/bin/mysql --user=root --password=$MYSQL_PASSWD -h $MYSQL_HOST < virtual_env/sql/setup_database.sql