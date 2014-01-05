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
# This script creates the default administrator account for Fantastico OAuth2 Identity Provider.
##############################################################################################################################

INSERT INTO oauth2_idp_persons(person_id, first_name, last_name, email_address)
SELECT 1, 'Fantastico', 'Admin', 'admin@fantastico.com'
FROM dual
WHERE 1 NOT IN (SELECT person_id FROM oauth2_idp_persons WHERE person_id = 1);

INSERT INTO oauth2_idp_users(user_id, username, `password`, person_id)
SELECT 1, 'admin@fantastico.com', 'ZjY5ZWVjOTNhZGNmOWExYWE5ZGE5YjAxNTRjMDJjN2Y5YjNmNjY4ZWQ0ZDA3MTVmMjMxZTAzNTQ1NDQ5YWI5MjA1NjhhYTEyMDkxYmIyZjJlNjE4OGUwMTg1MWFlNmJjZjkwMDVhOGZjZjJmZDEyZjRmMzAxYTdhYTFjMmNlNzg=',
	1
FROM dual
WHERE 1 NOT IN (SELECT user_id FROM oauth2_idp_users WHERE user_id = 1);

INSERT INTO oauth2_clients(client_id, `name`, description, grant_types, token_iv, token_key, revoked)
SELECT '11111111-1111-1111-1111-111111111111', 'Fantastico OAuth2 IDP', 
	   'This application provides the default identity provider for Fantastico.',
	   'token', 
	   '7U6DYcpSZw3SndbANJjeyg==',
       'UAWXxRuDM4ePqogFBHfJer3B9LwrilchQcs4kFVqBxE=',
	   False
FROM dual
WHERE '11111111-1111-1111-1111-111111111111' NOT IN (SELECT client_id FROM oauth2_clients WHERE client_id = '11111111-1111-1111-1111-111111111111');

INSERT INTO oauth2_client_returnurls (client_id, return_url)
SELECT '11111111-1111-1111-1111-111111111111', '/oauth/authorize'
FROM dual
WHERE NOT EXISTS(SELECT 1 
				 FROM oauth2_client_returnurls 
				 WHERE client_id = '11111111-1111-1111-1111-111111111111' AND
					   return_url = '/oauth/authorize');

INSERT INTO oauth2_scopes(scope_id, `name`)
SELECT 1, 'scope1'
FROM dual
WHERE NOT EXISTS(SELECT 1 FROM oauth2_scopes WHERE scope_id = 1);

INSERT INTO oauth2_client_scopes(client_id, scope_id)
SELECT '11111111-1111-1111-1111-111111111111', 1
FROM dual
WHERE NOT EXISTS(SELECT 1 
				 FROM oauth2_client_scopes
				 WHERE client_id = '11111111-1111-1111-1111-111111111111' AND
					   scope_id = 1);