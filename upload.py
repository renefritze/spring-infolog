# -*- coding: utf-8 -*-
from bottle import route,request,redirect
import bottle
from siteglobals import env, db,config
from utils import *
import hashlib,os
from zipfile import ZipFile
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
		upload_dir = config.get('site','uploads')
		fn = '%s/%s/%s.zip'%( os.getcwd(), upload_dir,hashlib.sha224(data).hexdigest() )
		fd = open( fn, 'wb')
		fd.write( data )
		fd.close()
		members = dict()
		zipfile = ZipFile( fn )

		files_of_interest = ['infolog.txt','ext.txt','platform.txt','script.txt','settings.txt','unitsync.log']
		for info in zipfile.infolist():
			if info.filename in files_of_interest and info.file_size < 20e5:
				members[info.filename] = zipfile.read( info.filename )
		db.parseZipMembers( fn, members )
		return 'success'

	except Exception, m:
		print m
		return env.get_template('error.html').render(err_msg=str(m))
