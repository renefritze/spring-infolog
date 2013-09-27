# Requirements
	* Python (tested on 2.6.4)
	* PasteServer
	* SqlAlchemy >=0.5
	* sqlite/mysql for db backend
	* Jinja2
	* bottle (included, newer will break auth)
	* paste
	* tw.forms
	* ToscaWidgets
	* baeker
	* genshi

A lot of these can be installed through pypi, eg. wiht python setuptools:

	easy_install {sprox,paste,tw.forms,ToscaWidgets,baeker,genshi}
	

# Usage
	* after cloning run: git submodule update --init
	* copy site.cfg.example to site.cfg and edit as necessary
	* run ./main.py
	* goto http://localhost:PORT (default PORT=4001)


	Copyright © 2013 <koshi@springlobby.info, braindamage@springlobby.info>
	This work is free. You can redistribute it and/or modify it under the
	terms of the Do What The Fuck You Want To Public License, Version 2,
	as published by Sam Hocevar. See the COPYING file for more details.
