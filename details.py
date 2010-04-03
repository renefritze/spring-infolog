# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env, db, config
from utils import *
from backend import Record

@route('/details', method='GET')
def output():
	try:
		session = db.sessionmaker()
		id = getSingleField( 'id', request )
		if not id:
			raise ElementNotFoundException( id )
		record = session.query( Record ).filter( Record.id == id ).one()
		if not record:
			raise ElementNotFoundException( id )
		upload_dir = config.get('site','uploads')
		ret = env.get_template('details.html').render( record=record, upload_dir=upload_dir )
		session.close()
		return ret

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

