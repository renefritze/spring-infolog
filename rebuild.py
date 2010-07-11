#!/usr/bin/env python
# -*- coding: utf-8 -*-
from siteglobals import db, config
from backend import *
from upload import parseZip
import os
db.Connect()

print 'DB: Rebuild init'
tables = [ Crash, RecordsData, Status, Settings, SettingsData, Stacktrace, StacktraceData, StacktraceTranslated, DbConfig ]
for table in tables:
	table.__table__.drop()
	table.__table__.create()
print 'DB: Rebuild completed'

print 'Upload: parseing init'
fn = os.getcwd() + "/" + config.get('site','uploads') + "/"
for filename in os.listdir(fn): 
	if filename[-4:] == '.zip':
		try:
			parseZip (config.get('site','uploads') + "/" + filename)
		except:
			print 'Upload: FAILED for ' + config.get('site','uploads') + "/" + filename
print 'Upload: parseing completed'
