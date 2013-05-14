#!/bin/bash

. pip-deps/bin/activate

/usr/bin/mysql --user=root --password=$MYSQL_PASSWD -h $MYSQL_HOST -v < virtual_env/sql/setup_database.sql

echo "Database Fantastico created correctly." 

find . -name 'module_setup.sql' | xargs /usr/bin/mysql --user=root --password=$MYSQL_PASSWD -h $MYSQL_HOST -v

echo "All module_setup.sql executed correctly."
