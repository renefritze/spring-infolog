#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, debug, PasteServer, send_file, redirect, abort, request, default_app
import os, index, upload
from siteglobals import config

@route('/images/:filename')
def image_file(filename):
	return send_file( filename, root=os.getcwd()+'/images/' )

@route('/static/:filename')
def static_file(filename):
	return send_file( filename, root=os.getcwd()+'/static/' )
	
@route('/favicon.ico')
def favi():
	return send_file( 'favicon.ico', root=os.getcwd()+'/images/' )

if __name__=="__main__":
	port = config.getint('site','port')
	app = default_app()
	run(app=app,server=PasteServer,host='localhost',port=port , reloader=True)