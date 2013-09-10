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
#
# This script is used to create dynamic pages required tables.
#
##############################################################################################################################

DROP TABLE IF EXISTS page_models;
DROP TABLE IF EXISTS pages;

CREATE TABLE pages(
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	url VARCHAR(100) NOT NULL,
	template VARCHAR(100) NOT NULL,
	keywords VARCHAR(200) NOT NULL,
	description VARCHAR(300) NOT NULL,
	title VARCHAR(100) NOT NULL,
	language VARCHAR(5) NOT NULL DEFAULT 'en',
	PRIMARY KEY (Id),
	CONSTRAINT unq_pages_url UNIQUE(url)
);

CREATE TABLE page_models(
	entry_id INT NOT NULL AUTO_INCREMENT,
	page_id INT NOT NULL,
	name VARCHAR(100) NOT NULL,
	value TEXT NOT NULL,
	PRIMARY KEY (entry_id, page_id),
	CONSTRAINT fk_pagemodels_page FOREIGN KEY (page_id) REFERENCES pages(id));

########## Insert a sample page also used for integration tests
INSERT INTO pages(id, name, url, template, keywords, description, title, language)
VALUES(1, '/test/default/page', '/test/default/page', '/dynamic_pages/views/sample_template.html', 'keyword1', 'description', 'title', 'ro-RO');

INSERT INTO page_models(page_id, name, value)
VALUES(1, 'article_title', 'article title');

INSERT INTO page_models(page_id, name, value)
VALUES(1, 'article_content', 'article content');