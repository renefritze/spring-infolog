# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import datetime, os, re, genshi

current_db_rev = 5
Base = declarative_base()

class Crash(Base):
	__tablename__ 			= 'records'
	id 						= Column( Integer, primary_key=True,index=True )
	date 					= Column( DateTime )
	extensions				= Column( Text )
	settings				= Column( Text )	# not used by PHP
	script					= Column( Text )
	filename				= Column( String(255) )
	platform				= Column( String(255) )
	spring					= Column( String(100) )
	map						= Column( String(100) )
	gamemod					= Column( String(100) )
	gameid					= Column( String(32) )
	sdl_version				= Column( String(100) )
	glew_version			= Column( String(100) )
	al_vendor				= Column( String(100) )
	al_version				= Column( String(100) )
	al_renderer				= Column( String(100) )
	al_extensions			= Column( Text )
	alc_extensions			= Column( String(255) )
	al_device				= Column( String(100) )
	al_available_devices	= Column( Text )
	gl_version				= Column( String(100) )
	gl_vendor				= Column( String(100) )
	gl_renderer				= Column( String(100) )
	crashed					= Column( Boolean, default=False )
	lobby_client_version	= Column( String(64) )
	contains_demo			= Column( Boolean, default=False )
	

	def __init__(self):
		self.date = datetime.datetime.now()
		
	def basename(self):
		return os.path.basename( self.filename )

	@property
	def id_link(self):
		return genshi.XML('<a href="/details?id=%s">%s</a>' % (self.id, str(self.date)))

class Status(Base):
	__tablename__	= 'status'
	internal_name	= Column( String(20), primary_key=True,index=True )
	display_name	= Column( String(60) )


class Settings(Base):
	__tablename__ 			= 'settings'
	id 						= Column( Integer, primary_key=True )
	setting					= Column( String(255), primary_key=True )
	value					= Column( String(255) )


class Stacktrace(Base):
	__tablename__ 			= 'stacktrace'
	id						= Column( Integer, primary_key=True )
	frame					= Column( Integer, primary_key=True )
	type					= Column( String(10), primary_key=True)
	line					= Column( Integer, primary_key=True )
	file					= Column( String(128) )
	functionname			= Column( String(128) )
	functionat				= Column( String(16) )
	address					= Column( String(10) )
	raw						= Column( String(255) )


class DbConfig(Base):
	__tablename__	= 'config'
	dbrevision		= Column( Integer, primary_key=True )

	def __init__(self):
		self.dbrevision = 1

class ElementExistsException( Exception ):
	def __init__(self, element):
		self.element = element

	def __str__(self):
		return "Element %s already exists in db"%(self.element)

class ElementNotFoundException( Exception ):
	def __init__(self, element):
		self.element = element

	def __str__(self):
		return "Element %s not found in db"%(self.element)

class DbConnectionLostException( Exception ):
	def __init__( self, trace ):
		self.trace = trace
	def __str__(self):
		return "Database connection temporarily lost during query"
	def getTrace(self):
		return self.trace

class Backend:
	def Connect(self):
		self.engine = create_engine(self.alchemy_uri, echo=self.verbose, pool_size=20, pool_recycle=300)
		self.metadata = Base.metadata
		self.metadata.bind = self.engine
		self.metadata.create_all(self.engine)
		self.sessionmaker = sessionmaker( bind=self.engine )

	def __init__(self,alchemy_uri,verbose=False):
		global current_db_rev
		self.alchemy_uri = alchemy_uri
		self.verbose = verbose
		self.Connect()
		oldrev = self.GetDBRevision()
		self.UpdateDBScheme( oldrev, current_db_rev )
		self.SetDBRevision( current_db_rev )

	def UpdateDBScheme( self, oldrev, current_db_rev ):
		pass

	def GetDBRevision(self):
		session = self.sessionmaker()
		rev = session.query( DbConfig.dbrevision ).order_by( DbConfig.dbrevision.desc() ).first()
		if not rev:
			#default value
			rev = -1
		else:
			rev = rev[0]
		session.close()
		return rev

	def SetDBRevision(self,rev):
		session = self.sessionmaker()
		conf = session.query( DbConfig ).first()
		if not conf:
			#default value
			conf = DbConfig()
		conf.dbrevision = rev
		session.add( conf )
		session.commit()
		session.close()

	def parseZipMembers(self, fn, data, date_time = '' ):
		session = self.sessionmaker()
		crash = Crash()
		crash.filename = fn
		session.add( crash )
		session.commit()
		crash_id = crash.id
		
		if (date_time):
			crash.date = datetime.datetime (date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5])
		
		if data.has_key( 'ext.txt' ):
			crash.extensions = self.dbEncode (data['ext.txt'])
		if data.has_key( 'script.txt' ):
			crash.script = self.dbEncode (data['script.txt'])
		if data.has_key( 'settings.txt' ):
			crash.settings = self.dbEncode (data['settings.txt'])
		crash.status = None
		
		if data.has_key ('client.txt'):
			temp = data['client.txt'].splitlines()
			if temp[0]:
				crash.lobby_client_version = self.dbEncode (temp[0])
		if data.has_key ('demo.sdf'):
			crash.contains_demo = True
		
		if data.has_key ('infolog.txt'):
			al_available_devices = []
			platform = []
			is_stacktrace = False
			stacktrace_type = ''
			stacktrace_key = 0
			
			for line in data['infolog.txt'].splitlines ():
				if re.search ('^OS: ', line):
					platform.append (self.parseInfologSub ('^OS: ', line))
				elif len (platform) == 1 and re.search ('^' + platform[0], line):
					platform[0] = line
				
				elif (re.search ('^\[[ 0]*\]', line)):
					value = self.parseInfologSub ('^\[[ 0]*\] Using map[ ]*', line)
					if (value):
						crash.map = self.dbEncode (value)
					if (not crash.gamemod):
						value = self.parseInfologSub ('^\[[ 0]*\] Using mod[ ]*', line)
						if (value):
							crash.gamemod = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] GameID:[ ]*', line)
					if (value):
						crash.gameid = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] SDL:[ ]*', line)
					if (value):
						crash.sdl_version = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] GLEW:[ ]*', line)
					if (value):
						crash.glew_version = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Vendor:[ ]*', line)
					if (value):
						crash.al_vendor = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Version:[ ]*', line)
					if (value):
						crash.al_version = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Renderer:[ ]*', line)
					if (value):
						crash.al_renderer = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*AL Extensions:[ ]*', line)
					if (value):
						crash.al_extensions = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*ALC Extensions:[ ]*', line)
					if (value):
						crash.alc_extensions = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Device:[ ]*', line)
					if (value):
						crash.al_device = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]{23}', line)
					if (value):
						al_available_devices.append (value)
					value = self.parseInfologSub ('^\[[ 0]*\] GL:[ ]*', line)
					if (value):
						if (not crash.gl_version):
							crash.gl_version = self.dbEncode (value)
						elif (not crash.gl_vendor):
							crash.gl_vendor = self.dbEncode (value)
						elif (not crash.gl_renderer):
							crash.gl_renderer = self.dbEncode (value)
				elif (not crash.spring):
					match = re.search ('^Spring(/d*\.)*', line)
					if (match):
						crash.spring = self.dbEncode (line)
				elif (crash.spring):
					match = re.search ('^\[[ 0-9]*\] Spring( /d*\.)*.*has crashed.$', line)
					if (match):
						crash.crashed = True
				
				match = re.search ('^\[[ 0-9]*\] Stacktrace \(', line)
				if (match):
					is_stacktrace = True
					stacktrace_type = 'sim'
				else:
					match = re.search ('^\[[ 0-9]*\] Stacktrace:', line)
					if (match):
						is_stacktrace = True
						stacktrace_type = 'regular'
					elif (is_stacktrace and re.search ('^\[[ 0-9]*\] \([0-9]*\) ', line)):
						stacktrace_key = int (self.parseInfologSub ('^\[[ 0-9]*\]', line, 0)[1:-1])
						temp = {}
						value = self.parseInfologSub ('^\[[ 0-9]*\] ', line)
						value = value.split (' ')
						temp['line'] = value[0][1:-1]
						temp['address'] = value[len (value) - 1][1:-1]
						if (value[len (value) - 2][-1] == ')'):
							temp['file'] = value[len (value) - 2][:value[len (value) - 2].rfind ('(')]
							temp['function'] = value[len (value) - 2][value[len (value) - 2].rfind ('(') + 1:value[len (value) - 2].rfind ('+')]
							temp['functionat'] = value[len (value) - 2][value[len (value) - 2].rfind ('+') + 1:-1]
						else:
							temp['file'] = value[len (value) - 2]
						temp['file'] = temp['file'][max (temp['file'].rfind ('\\'), temp['file'].rfind ('/')) + 1:]
						
						stacktrace = Stacktrace()
						stacktrace.id = crash.id
						stacktrace.frame = stacktrace_key
						stacktrace.type = stacktrace_type
						stacktrace.raw = self.dbEncode (line)
						stacktrace.line = int (temp['line'])
						stacktrace.file = temp['file']
						if (temp.has_key ('function')):
							stacktrace.functionname = temp['function']
						if (temp.has_key ('functionat')):
							stacktrace.functionat = temp['functionat']
						stacktrace.address = temp['address']
						session.add( stacktrace )
						session.commit()

				
			if (al_available_devices):
				crash.al_available_devices = self.dbEncode ("\n".join (al_available_devices))
			if platform and not re.search ('^Linux', platform[0]):
				crash.platform = self.dbEncode (' '.join (platform))
			elif not data.has_key( 'platform.txt' ):
				crash.platform = self.dbEncode (' '.join (platform))
			else:
				crash.platform = self.dbEncode (data['platform.txt'].strip ())
		
		session.add( crash )
		session.commit()
		
		if data.has_key ('settings.txt'):
			set_settings = {}
			for x in data['settings.txt'].splitlines ():
				if x and x.index ('=') != -1 and x[:x.index ('=')]:
					key = x[:x.index ('=')].lower ()
					if not set_settings.has_key (key):
						settings = Settings()
						settings.id = crash.id
						settings.setting = x[:x.index ('=')]
						settings.value = x[x.index ('=') + 1:]
						set_settings[key] = 1
						session.add( settings )
						session.commit()

		session.close()
		return crash_id
	
	
	def parseInfologSub (self, preg, line, removematch = 1):
		match = re.search (preg, line)
		if (match):
			if (removematch):
				return (line.replace (match.group (0), ''))
			else:
				return (match.group (0))
	
	def dbEncode (Self, string):
		try:
			return (string.encode('utf8'))
		except:
			return ('ufc error')