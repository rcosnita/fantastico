#!/bin/bash

. pip-deps/bin/activate

/usr/bin/mysql --user=root --password=$MYSQL_PASSWD -h $MYSQL_HOST -v < virtual_env/sql/setup_database.sql

echo "Database Fantastico created correctly." 

./fsdk syncdb --db-command /usr/bin/mysql --comp-root fantastico

echo "All module_setup.sql executed correctly."
