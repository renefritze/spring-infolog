# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env, db
from utils import *
import tempfile

@route('/upload', method='GET')
def output():
	try:
		return env.get_template('upload.html').render( )

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

@route('/upload', method='POST')
def output_post():
	try:
		#datafile = request.POST.get('infolog')
		datafile = request.POST['infolog'].value.split()
		#tmp = tempfile.NamedTemporaryFile( 'wr' )
		#for l in (filter( lambda p: p != '\n',datafile) ):
			#tmp.write( l.replace('\n','') )
		#tmp.seek(0)
		db.parseInfolog( datafile )
		return str(datafile)

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))
