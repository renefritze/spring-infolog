# -*- coding: utf-8 -*-
from bottle import route,request,redirect
import bottle
from siteglobals import env, db,config
from utils import *
import hashlib,os

@route('/upload', method='GET')
def output():
	try:
		return env.get_template('upload.html').render( )

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

@route('/upload', method='POST')
def output_post():
	try:
		data = request.POST['file'].value
		fn = '%s/%s/%s.zip'%( os.getcwd(), config.get('site','uploads'),hashlib.sha224(data).hexdigest() )
		fd = open( fn, 'wb')
		fd.write( data )
		fd.close()
		#db.parseInfolog( fn )
		return 'success'

	except Exception, m:
		print m
		return env.get_template('error.html').render(err_msg=str(m))
