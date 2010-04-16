#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, debug, PasteServer, send_file, redirect, abort, request, default_app
import os, index, upload, recordlist, details
from siteglobals import config,is_debug
from tw.api import make_middleware

@route('/images/:filename')
def image_file(filename):
	return send_file( filename, root=os.getcwd()+'/images/' )

@route('/static/:filename')
def static_file(filename):
	return send_file( filename, root=os.getcwd()+'/static/' )

uploads = '/%s/' % config.get('site','uploads')
@route(uploads + ':filename')
def log_file(filename):
	return send_file( filename, root=os.getcwd()+ uploads )

@route('/favicon.ico')
def favi():
	return send_file( 'favicon.ico', root=os.getcwd()+'/images/' )

if __name__=="__main__":
	port = config.getint('site','port')
	host = config.get('site','host')
	app = default_app()
	application = make_middleware(app, {
		'toscawidgets.framework.default_view': 'jinja2',
		'toscawidgets.middleware.inject_resources': True,
		}, stack_registry=True)
	debug(is_debug)
	run(app=application,server=PasteServer,host=host,port=port , reloader=is_debug)	
