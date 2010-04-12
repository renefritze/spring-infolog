# -*- coding: utf-8 -*-
from bottle import route,request
from siteglobals import env, db, config
from utils import *
from backend import Crash
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller

class CrashTableFiller(TableFiller):
	__model__ = Crash

	def date(self,crash):
		dates = '<a href="/details?id=%d">%s</a>'%(crash.id,str(crash.date))
		return dates
class CrashTable( TableBase ):
	__model__	= Crash
	__omit_fields__ = ['id', 'extensions', '__actions__','settings','filename','script']
	__xml_fields__=['date']

@route('/list', method='GET')
def output():
	try:
		session = db.sessionmaker()
		crash_table = CrashTable(session)
		crash_filler = CrashTableFiller(session)
		ret = env.get_template('list.html').render( widget=crash_table, value=crash_filler.get_value() )
		session.close()
		return ret

	except Exception, m:
		return env.get_template('error.html').render(err_msg=str(m))
