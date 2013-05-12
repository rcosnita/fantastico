##############################################################################################################################
# Copyright 2013 Cosnita Radu Viorel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##############################################################################################################################

##############################################################################################################################
# This script holds the create database script for fantastico core framework. This database is required for making
# all other integration tests run as expected. In addition it creates a default user that can manage / access this
# database.
##############################################################################################################################

DROP DATABASE IF EXISTS fantastico;

CREATE DATABASE IF NOT EXISTS fantastico
	DEFAULT CHARACTER SET utf8
	DEFAULT COLLATE utf8_general_ci;

USE fantastico;

DELIMITER $$

CREATE PROCEDURE spr_setup_db()
BEGIN
	DECLARE user_exist INT DEFAULT 0;

	SELECT 1 INTO user_exist FROM mysql.user WHERE User = 'fantastico' AND Host = '%';

	IF user_exist = 1 THEN
		DROP USER 'fantastico'@'%';
	END IF;

	CREATE USER 'fantastico'@'%' IDENTIFIED BY '12345';
	GRANT ALL PRIVILEGES ON fantastico.* TO 'fantastico'@'%';
END $$

DELIMITER ;

CALL spr_setup_db();
DROP PROCEDURE spr_setup_db;