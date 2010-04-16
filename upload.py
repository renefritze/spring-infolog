#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route,request,redirect
import bottle
from siteglobals import env, db,config,tasbot,cache
from utils import *
import hashlib,os,sys
from zipfile import ZipFile
import recordlist
@route('/upload', method='GET')
def output():
	try:
		return env.get_template('upload.html').render( )

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

def parseZip( fn ):
	date_time = ''
	members = dict()
	zipfile = ZipFile( fn )
	cache.invalidate(recordlist.output, 'list_output', )
	files_of_interest = ['infolog.txt','ext.txt','platform.txt','script.txt','settings.txt','unitsync.log']
	for info in zipfile.infolist():
		if info.filename in files_of_interest and info.file_size < 20e5:
			members[info.filename] = zipfile.read( info.filename )
			if info.filename == 'infolog.txt':
				date_time = info.date_time
	return db.parseZipMembers( fn, members, date_time )

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
	failed = []
	sys.stdout.write( 'parsing' )
	for fn in sys.argv[1:]:
		try:
			sys.stdout.write( '.' )
			sys.stdout.flush()
			parseZip( fn )
		except Exception, e:
			failed.append( 'failed: %s: %s'%(fn, str(e) ) )
	print '\nsuccesfully imported %d of %d records'%(len(sys.argv[1:]) - len(failed), len(sys.argv[1:]) )
	print '\n'.join(failed)