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
# This script creates Menus and MenuItems tables required for supporting dynamic menus component. For more information, read
# official Fantastico documentation.
##############################################################################################################################

CREATE TABLE menus(
	id INTEGER AUTO_INCREMENT,
	name VARCHAR(150),
	PRIMARY KEY(id)
);

CREATE TABLE menu_items(
	id INTEGER AUTO_INCREMENT,
	target VARCHAR(50) NOT NULL DEFAULT '_blank',
	url VARCHAR(255) NOT NULL,
	title VARCHAR(255) NOT NULL,
	label VARCHAR(255) NOT NULL,
	menu_id INTEGER NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_menuitems_menu FOREIGN KEY(menu_id) REFERENCES menus(id)
);