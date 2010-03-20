#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env

@route('/')
def output():
	try:
		return env.get_template('index.html').render( )
		
	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

