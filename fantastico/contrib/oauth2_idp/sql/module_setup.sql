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
# This script creates the tables for Fantastico OAuth2 Identity Provider.
##############################################################################################################################

CREATE TABLE IF NOT EXISTS oauth2_idp_persons(
	person_id INTEGER NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email_address VARCHAR(100),
	cell_number VARCHAR(30),
	phone_number VARCHAR(30),
	PRIMARY KEY(person_id),
	CONSTRAINT unq_firstlast_name_email UNIQUE(first_name, last_name, email_address)
);

CREATE TABLE IF NOT EXISTS oauth2_idp_users(
	user_id INTEGER NOT NULL AUTO_INCREMENT,
	username VARCHAR(100) NOT NULL,
	`password` VARCHAR(256) NOT NULL,
	person_id INTEGER NOT NULL,
	PRIMARY KEY(user_id),
	CONSTRAINT unq_users_username UNIQUE(username),
	CONSTRAINT fk_users_person FOREIGN KEY(person_id) REFERENCES oauth2_idp_persons(person_id)
);

CREATE TABLE IF NOT EXISTS oauth2_clients(
	client_id VARCHAR(36) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	description LONGTEXT NOT NULL,
	grant_types VARCHAR(200) NOT NULL,
	token_iv VARCHAR(256) NOT NULL,
	token_key VARCHAR(256) NOT NULL,
	revoked BOOLEAN NOT NULL DEFAULT False,
	PRIMARY KEY(client_id),
	CONSTRAINT unq_clients_name UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS oauth2_client_returnurls(
	url_id INTEGER NOT NULL AUTO_INCREMENT,
	client_id VARCHAR(36) NOT NULL,
	return_url VARCHAR(255) NOT NULL,
	PRIMARY KEY(url_id),
	CONSTRAINT unq_clientreturnurls_clienturl UNIQUE(client_id, return_url),
	CONSTRAINT fk_clientreturnurls_client FOREIGN KEY(client_id) REFERENCES oauth2_clients(client_id)
);

CREATE TABLE IF NOT EXISTS oauth2_scopes(
	scope_id INTEGER AUTO_INCREMENT NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	description LONGTEXT,
	PRIMARY KEY(scope_id),
	CONSTRAINT unq_oauth2scopes_name UNIQUE(`name`)
);

CREATE TABLE IF NOT EXISTS oauth2_client_scopes(
	client_id VARCHAR(36) NOT NULL,
	scope_id INTEGER NOT NULL,
	PRIMARY KEY(client_id, scope_id),
	CONSTRAINT fk_oauth2clientscopes_client FOREIGN KEY(client_id) REFERENCES oauth2_clients(client_id),
	CONSTRAINT fk_oauth2clientscopes_scope FOREIGN KEY(scope_id) REFERENCES oauth2_scopes(scope_id)
);