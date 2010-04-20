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
#	extensions				= Column( PickleType )
#	settings				= Column( PickleType )
#	script					= Column( PickleType )
	extensions				= Column( Text )
	settings				= Column( Text )
	script					= Column( Text )
	filename				= Column( String(255) )
	platform				= Column( String(100) )
	spring					= Column( String(100) )
	map						= Column( String(100) )
	gamemod					= Column( String(100) )
	gameid					= Column( String(100) )
	sdl_version				= Column( String(100) )
	glew_version			= Column( String(100) )
	al_vendor				= Column( String(100) )
	al_version				= Column( String(100) )
	al_renderer				= Column( String(100) )
	al_extensions			= Column( String(255) )
	alc_extensions			= Column( String(255) )
	al_device				= Column( String(100) )
	al_available_devices	= Column( Text )
	gl_version				= Column( String(100) )
	gl_vendor				= Column( String(100) )
	gl_renderer				= Column( String(100) )
	crashed					= Column( Boolean, default=False )
	lobby_client_version	= Column ( String(30) )
	

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
		self.engine = create_engine(self.alchemy_uri, echo=self.verbose)
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
			crash.extensions = data['ext.txt']
		if data.has_key( 'script.txt' ):
			crash.script = data['script.txt']
		if data.has_key( 'settings.txt' ):
			crash.settings = data['settings.txt']
		if data.has_key( 'platform.txt' ):
			crash.platform = data['platform.txt'].strip()
		crash.status = None
		
		if data.has_key ('client.txt'):
			temp = data['client.txt'].splitlines()
			if temp[0]:
				crash.lobby_client_version = temp[0]
		
		if data.has_key ('infolog.txt'):
			al_available_devices = []
			for line in data['infolog.txt'].splitlines ():
				if (re.search ('^\[[ 0]*\]', line)):
					value = self.parseInfologSub ('^\[[ 0]*\] Using map[ ]*', line)
					if (value):
						crash.map = self.dbEncode (value)
					if (not crash.gamemod):
						value = self.parseInfologSub ('^\[[ 0]*\] Using mod[ ]*', line)
						if (value):
							crash.gamemod = self.dbEncode (value)
					value = self.parseInfologSub ('^\[[ 0]*\] GameID:[ ]*', line)
					if (value):
						self.gameid = self.dbEncode (value)
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
			if (al_available_devices):
				crash.al_available_devices = self.dbEncode ("\n".join (al_available_devices))
		
		session.add( crash )
		session.commit()
		session.close()
		return crash_id
	
	
	def parseInfologSub (self, preg, line):
		match = re.search (preg, line)
		if (match):
			return (line.replace (match.group (0), ''))
	
	
	def dbEncode (Self, string):
		try:
			return (string.encode('utf8'))
		except:
			return ('ufc error')