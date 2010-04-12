#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route,request,redirect
import bottle
from siteglobals import env, db,config,tasbot
from utils import *
import hashlib,os,sys
from zipfile import ZipFile
@route('/upload', method='GET')
def output():
	try:
		return env.get_template('upload.html').render( )

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

def parseZip( fn ):
	members = dict()
	zipfile = ZipFile( fn )

	files_of_interest = ['infolog.txt','ext.txt','platform.txt','script.txt','settings.txt','unitsync.log']
	for info in zipfile.infolist():
		if info.filename in files_of_interest and info.file_size < 20e5:
			members[info.filename] = zipfile.read( info.filename )
	return db.parseZipMembers( fn, members )

@route('/upload', method='POST')
def output_post():
	try:
		data = request.POST['file'].value
		upload_dir = config.get('site','uploads')
		fn = '%s/%s/%s.zip'%( os.getcwd(), upload_dir,hashlib.sha224(data).hexdigest() )
		fd = open( fn, 'wb')
		fd.write( data )
		fd.close()
		new_id = parseZip( fn )
		base_url = config.get('site', 'baseurl' )
		chan = config.get('tasbot', 'report_channel' )
		tasbot.tasclient.say(chan,'new crash report uploaded: http://%s/details?id=%d'%(base_url,new_id))
		return 'success'

	except Exception, m:
		print m
		return env.get_template('error.html').render(err_msg=str(m))

if __name__=="__main__":
	for fn in sys.argv[1:]:
		try:
			print 'parsing %s'%fn
			parseZip( fn )
			print '\t...done'
		except Exception, e:
			print '\tfailed: %s'%str(e)