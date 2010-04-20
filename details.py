# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env, db, config
from utils import *
from backend import Crash

@route('/details', method='GET')
def output():
	try:
		important_settings = ['Shadows']

		session = db.sessionmaker()
		id = getSingleField( 'id', request )
		if not id:
			raise ElementNotFoundException( id )
		crash = session.query( Crash ).filter( Crash.id == id ).one()
		if not crash:
			raise ElementNotFoundException( id )
		upload_dir = config.get('site','uploads')
		ret = env.get_template('details.html').render( crash=crash, \
			upload_dir=upload_dir,settings=dict(filter(lambda i: i[0] in important_settings, dict( zip( map( lambda line: line.split('=')[0], crash.settings.splitlines() ), map( lambda line: line.split('=')[1], crash.settings.splitlines() ) ) ).items () ) ) )
		session.close()
		return ret

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))

