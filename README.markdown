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
