# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env, db, config, cache
from utils import *
from backend import Crash
import tw.forms as twf, tw.dynforms as twd

class CrashGrid(twd.FilteringGrid):
	datasrc = lambda s: db.sessionmaker().query(Crash).filter( Crash.crashed == True )
	columns = [('id_link','Date'), ('spring', 'rev.'), ('platform','Platform'),('gl_vendor','GL vendor'),('mod','Mod'),('map','Map')]#,('nick', 'Reporter')]
	data_filter = ['map', 'mod','spring','platform',]
	search_cols = ['settings','extensions']

@cache.cache('list_output', expire=60)
@route('/list', method='GET')
@route('/list', method='POST')
def output():
	try:
		crash_grid = CrashGrid('Crashes')
		ret = env.get_template('list.html').render( crash_grid=crash_grid, kw=dict(request.POST) )
		return ret

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))
