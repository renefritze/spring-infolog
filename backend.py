# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import datetime, os, re, genshi, xmlrpclib, time

current_db_rev = 5
Base = declarative_base()

class Crash(Base):
	__tablename__ 			= 'records'
	id						= Column( Integer, primary_key=True )
	date					= Column( DateTime )
	filename				= Column( String(255) )
	script					= Column( Text )
	playerid				= Column( Integer )
	extensionsid			= Column( Integer )
	platformid				= Column( Integer )
	springid				= Column( Integer )
	mapid					= Column( Integer )
	gamemodid				= Column( Integer )
	gameidid				= Column( Integer )
	sdl_versionid			= Column( Integer )
	glew_versionid			= Column( Integer )
	al_vendorid				= Column( Integer )
	al_versionid			= Column( Integer )
	al_rendererid			= Column( Integer )
	al_extensionsid			= Column( Integer )
	alc_extensionsid		= Column( Integer )
	al_deviceid				= Column( Integer )
	al_available_devicesid	= Column( Integer )
	gl_versionid			= Column( Integer )
	gl_vendorid				= Column( Integer )
	gl_rendererid			= Column( Integer )
	lobby_client_versionid	= Column( Integer )
	first_crash_lineid		= Column( Integer )
	first_crash_line_translatedid	= Column( Integer )
	crashed					= Column( Boolean, default=False )
	contains_demo			= Column( Boolean, default=False )
	springversion			= ''	# Contains the spring version string
	
#	settings = relation( 'Settings', order_by='Settings.setting.desc' )
#	stacktrace = relation( 'Stacktrace', order_by='Stacktrace.frame' )

	def __init__(self):
		self.date = datetime.datetime.now()
		
	def basename(self):
		return os.path.basename( self.filename )

	@property
	def id_link(self):
		return genshi.XML('<a href="/details?id=%s">%s</a>' % (self.id, str(self.date)))


class RecordsData(Base):
	__tablename__ 			= 'recordsdata'
	id						= Column( Integer, primary_key=True )
	field					= Column( Enum ('extensions', 'platform', 'spring', 'map', 'gamemod', 'gameid' ,'sdl_version' ,'glew_version' ,'al_vendor' ,'al_version' ,'al_renderer' ,'al_extensions' ,'alc_extensions' ,'al_device' ,'al_available_devices' ,'gl_version' ,'gl_vendor' ,'gl_renderer' ,'lobby_client_version', 'first_crash_line', 'first_crash_line_translated', 'player') )
	data					= Column( Text )


class Status(Base):
	__tablename__			= 'status'
	internal_name			= Column( String(20), primary_key=True )
	display_name			= Column( String(60) )


class Settings(Base):
	__tablename__ 			= 'settings'
	reportid				= Column( Integer, ForeignKey( Crash.id ), primary_key=True )
	settingid				= Column( Integer, primary_key=True )
	valueid					= Column (Integer )


class SettingsData(Base):
	__tablename__ 			= 'settingsdata'
	id						= Column( Integer, primary_key=True )
	type					= Column( Enum ('setting', 'value') )
	data					= Column( String(255) )


class Stacktrace(Base):
	__tablename__ 			= 'stacktrace'
	reportid				= Column( Integer, ForeignKey( Crash.id ), primary_key=True )
	orderid					= Column( Integer, primary_key=True )
	stacktraceid			= Column( Integer )
	translatedid			= Column( Integer )
	type					= Column( String(10))
	line					= Column( Integer )
	raw						= Column( String(255) )
	function				= ''
	address					= ''


class StacktraceData(Base):
	__tablename__ 			= 'stacktracedata'
	id						= Column( Integer, primary_key=True )
	file					= Column( String(128) )
	functionname			= Column( String(128) )
	functionaddress			= Column( String(16) )
	address					= Column( String(10) )


class StacktraceTranslated(Base):
	__tablename__ 			= 'stacktracetranslated'
	id						= Column( Integer, primary_key=True )
	file					= Column( String(128) )
	line					= Column( Integer )


class CacheStacktrace(Base):
	__tablename__ 			= 'cachestacktrace'
	id						= Column( Integer, primary_key=True )
	spring					= Column( String(128) )
	file					= Column( String(128) )
	address					= Column( String(10) )
	cppfile					= Column( String(128) )
	cppline					= Column( Integer )
	lastscan				= Column( Integer )
	successful				= Column( Boolean, default=False )


class Cache(Base):
	__tablename__ 			= 'cache'
	Field					= Column ( String(128), primary_key=True )
	Data					= Column ( Text(200000) )
	Updated					= Column ( Integer )
	

class DbConfig(Base):
	__tablename__			= 'config'
	dbrevision				= Column( Integer, primary_key=True )

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
		self.getSettingIDCache = {}
		self.getStacktraceIDCache = {}
		self.getRecordDataIDCache = {}
		self.getCacheTranslateStacktraceCache = {}
		self.TranslateStacktraceCache = {}
	

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
			crash.extensionsid = self.getRecordDataID (session, 'extensions', data['ext.txt'])
		if data.has_key( 'script.txt' ):
			crash.script = self.dbEncode (data['script.txt'])
			for line in data['script.txt'].split ():
				if line.find ('MyPlayerName') != -1:
					crash.playerid = self.getRecordDataID (session, 'player', line.strip ()[13:-1])
		
		crash.status = None
		
		if data.has_key ('client.txt'):
			temp = data['client.txt'].splitlines()
			if temp[0]:
				crash.lobby_client_versionid = self.getRecordDataID (session, 'lobby_client_version', temp[0])

		if data.has_key ('demo.sdf'):
			crash.contains_demo = True
		
		if data.has_key ('infolog.txt'):
			al_available_devices = []
			platform = []
			is_stacktrace = False
			stacktrace_type = ''
			stacktrace_key = 0
			stacktrace_id = 0
			stacktracelist = []
			springline = ''
			
			for line in data['infolog.txt'].splitlines ():
				if re.search ('^OS: ', line):
					platform.append (self.parseInfologSub ('^OS: ', line))
				elif len (platform) == 1 and re.search ('^' + platform[0], line):
					platform[0] = line
				
				elif (re.search ('^\[[ 0]*\]', line)):
					value = self.parseInfologSub ('^\[[ 0]*\] Using map[ ]*', line)
					if (value):
						crash.mapid = self.getRecordDataID (session, 'map', value)
					if (not crash.gamemodid):
						value = self.parseInfologSub ('^\[[ 0]*\] Using mod[ ]*', line)
						if (value):
							crash.gamemodid = self.getRecordDataID (session, 'gamemod', value)
					value = self.parseInfologSub ('^\[[ 0]*\] GameID:[ ]*', line)
					if (value):
						crash.gameidid = self.getRecordDataID (session, 'gameid', value)
					value = self.parseInfologSub ('^\[[ 0]*\] SDL:[ ]*', line)
					if (value):
						crash.sdl_versionid = self.getRecordDataID (session, 'sdl_version', value)
					value = self.parseInfologSub ('^\[[ 0]*\] GLEW:[ ]*', line)
					if (value):
						crash.glew_versionid = self.getRecordDataID (session, 'glew_version', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Vendor:[ ]*', line)
					if (value):
						crash.al_vendorid = self.getRecordDataID (session, 'al_vendor', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Version:[ ]*', line)
					if (value):
						crash.al_versionid = self.getRecordDataID (session, 'al_version', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Renderer:[ ]*', line)
					if (value):
						crash.al_rendererid = self.getRecordDataID (session, 'al_renderer', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*AL Extensions:[ ]*', line)
					if (value):
						crash.al_extensionsid = self.getRecordDataID (session, 'al_extensions', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*ALC Extensions:[ ]*', line)
					if (value):
						crash.alc_extensionsid = self.getRecordDataID (session, 'alc_extensions', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]*Device:[ ]*', line)
					if (value):
						crash.al_deviceid = self.getRecordDataID (session, 'al_device', value)
					value = self.parseInfologSub ('^\[[ 0]*\] Sound:[ ]{23}', line)
					if (value):
						al_available_devices.append (value)
					value = self.parseInfologSub ('^\[[ 0]*\] GL:[ ]*', line)
					if (value):
						if (not crash.gl_versionid):
							crash.gl_versionid = self.getRecordDataID (session, 'gl_version', value)
						elif (not crash.gl_vendorid):
							crash.gl_vendorid = self.getRecordDataID (session, 'gl_vendor', value)
						elif (not crash.gl_rendererid):
							crash.gl_rendererid = self.getRecordDataID (session, 'gl_renderer', value)
				elif (not crash.springid):
					match = re.search ('^Spring(/d*\.)*', line)
					if (match):
						crash.springid = self.getRecordDataID (session, 'spring', line)
						crash.springversion = line
				if (crash.springid and not crash.crashed):
					match = re.search ('^\[[ 0-9]*\] Spring( /d*\.)*.*has crashed.$', line)
					if (match):
						crash.crashed = True
						springline = line
				
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
						stacktrace_id = stacktrace_id + 1
						stacktrace_key = int (self.parseInfologSub ('^\[[ 0-9]*\]', line, 0)[1:-1])
						temp = {'function':None, 'functionat':None}
						value = self.parseInfologSub ('^\[[ 0-9]*\] ', line)
						value = value.split (' ')
						temp['line'] = value[0][1:-1]
						temp['address'] = value[len (value) - 1][1:-1]
						if (value[len (value) - 2][-1] == ')'):
							temp['function'] = value[len (value) - 2][value[len (value) - 2].rfind ('(') + 1:value[len (value) - 2].rfind ('+')]
							temp['functionat'] = value[len (value) - 2][value[len (value) - 2].rfind ('+') + 1:-1]
						
						temp['file'] = self.parseInfologSub ('^\[[ 0-9]*\] \([0-9]*\) ', line)
						temp['file'] = temp['file'].replace ('[' + temp['address'] + ']', '').replace ('(' + str (temp['function']) + '+' + str (temp['functionat']) + ')', '').strip ()
						
						stacktrace = Stacktrace()
						stacktrace.reportid = crash.id
						stacktrace.orderid = stacktrace_id
						stacktrace.stacktraceid = self.getStacktraceID (session, temp['file'], temp['address'], temp['function'], temp['functionat'])
						stacktrace.type = stacktrace_type
						stacktrace.line = int (temp['line'])
						stacktrace.raw = line
						stacktrace.function = temp['file']
						stacktrace.address = temp['address']
						stacktracelist.append ( stacktrace )
						
						# First line for grouping reasons... (containing \AI\Skirmish\ or spring.exe)
						if not crash.first_crash_lineid:
							match = self.findSpringModuleFile (line)
							if (match):
								crash.first_crash_lineid = self.getRecordDataID (session, 'first_crash_line', match + ' [' + temp['address'] + ']')
								trans = self.getCacheTranslateStacktrace (session, crash.springversion, match, temp['address'])
								if trans['successful']:
									crash.first_crash_line_translatedid = self.getRecordDataID (session, 'first_crash_line_translated', trans['file'] + ' (' + str (trans['line']) + ')')
			
			if (al_available_devices):
				crash.al_available_devicesid = self.getRecordDataID (session, 'al_available_devices', "\n".join (al_available_devices))
			if platform and not re.search ('^Linux', platform[0]):
				crash.platformid = self.getRecordDataID (session, 'platform', ' '.join (platform))
			elif not data.has_key( 'platform.txt' ):
				crash.platformid = self.getRecordDataID (session, 'platform', ' '.join (platform))
			else:
				crash.platformid = self.getRecordDataID (session, 'platform', data['platform.txt'].strip ())
		
			if len (stacktracelist) > 0:
				stacktracelist = self.translateStacktrace (session, crash.springversion, stacktracelist)
				session.add_all( stacktracelist )
				session.commit()

		session.add( crash )
		session.commit()
		
		settingslist = []
		if data.has_key ('settings.txt'):
			set_settings = {}
			for x in data['settings.txt'].splitlines ():
				if x and x.index ('=') != -1 and x[:x.index ('=')]:
					key = x[:x.index ('=')].lower ()
					if not set_settings.has_key (key):
						settings = Settings()
						settings.reportid = crash.id
						settings.settingid = self.getSettingID (session, 'setting', x[:x.index ('=')])
						settings.valueid = self.getSettingID (session, 'value', x[x.index ('=') + 1:])
						set_settings[key] = 1
						settingslist.append( settings )
		
			session.add_all( settingslist )
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
	
	
	def getSettingID (self, session, type, data):
		if self.getSettingIDCache.has_key (type):
			if self.getSettingIDCache[type].has_key (data):
				return (self.getSettingIDCache[type][data])
		
		id = session.query( SettingsData.id ).filter( SettingsData.type == type ).filter(  SettingsData.data == data ).first()
		try:
			if session.query( SettingsData.id ).filter( and_ (SettingsData.type == type, SettingsData.data == data ) ).one():
				if not self.getSettingIDCache.has_key (type):
					self.getSettingIDCache[type] = {}
				self.getSettingIDCache[type][data] = id.id
				return (id.id)
		except:
			settingsdata = SettingsData()
			settingsdata.type = type
			settingsdata.data = data
			session.add( settingsdata )
			session.commit()
			return (settingsdata.id)


	def getStacktraceID (self, session, file, address, functionname, functionaddress):
		if self.getStacktraceIDCache.has_key (file):
			if self.getStacktraceIDCache[file].has_key (address):
				if self.getStacktraceIDCache[file][address].has_key (functionname):
					if self.getStacktraceIDCache[file][address][functionname].has_key (functionaddress):
						return (self.getStacktraceIDCache[file][address][functionname][functionaddress])
					
		
		id = session.query( StacktraceData.id ).filter( StacktraceData.file == file ).filter( StacktraceData.address == address ).filter ( StacktraceData.functionname == functionname ).filter ( StacktraceData.functionaddress == functionaddress ).first()
		try:
			if session.query( StacktraceData.id ).filter( and_ (StacktraceData.file == file, StacktraceData.address == address, StacktraceData.functionname == functionname, StacktraceData.functionaddress == functionaddress ) ).one():
				if not self.getStacktraceIDCache.has_key (file):
					self.getStacktraceIDCache[file] = {}
				if not self.getStacktraceIDCache[file].has_key (address):
					self.getStacktraceIDCache[file][address] = {}
				if not self.getStacktraceIDCache[file][address].has_key (functionname):
					self.getStacktraceIDCache[file][address][functionname] = {}
				self.getStacktraceIDCache[file][address][functionname][functionaddress] = id.id
				return (id.id)
		except:
			stacktracedata = StacktraceData()
			stacktracedata.file = file
			stacktracedata.address = address
			stacktracedata.functionname = functionname
			stacktracedata.functionaddress = functionaddress
			session.add( stacktracedata )
			session.commit()
			return (stacktracedata.id)


	def getRecordDataID (self, session, field, data):
		field = self.dbEncode (field)
		data = self.dbEncode (data).strip ()
		if not data:
			return (None)
		if self.getRecordDataIDCache.has_key (field):
			if self.getRecordDataIDCache[field].has_key (data):
				return (self.getRecordDataIDCache[field][data])
		
		id = session.query( RecordsData.id ).filter( RecordsData.field == field ).filter( RecordsData.data == data ).first()
		try:
			if session.query( RecordsData.id ).filter( and_ (RecordsData.field == field, RecordsData.data == data ) ).one():
				if not self.getRecordDataIDCache.has_key (field):
					self.getRecordDataIDCache[field] = {}
				self.getRecordDataIDCache[field][data] = id.id
				return (id.id)
		except:
			recordsdata = RecordsData()
			recordsdata.field = field
			recordsdata.data = data
			session.add( recordsdata )
			session.commit()
			return (recordsdata.id)
	
	
	def translateStacktrace (self, session, springversion, stacktracelist):
		for stacktrace in stacktracelist:
			stacktrace.translatedid = self.getTranslateStacktrace (session, springversion, stacktrace.function, stacktrace.address)
		return (stacktracelist)
	
	
	def getTranslateStacktrace (self, session, springversion, function, address):
		id = None
		result = self.getCacheTranslateStacktrace (session, springversion, function, address)
		if (result):
			if result['successful']:
				if self.TranslateStacktraceCache.has_key (result['file']):
					if self.TranslateStacktraceCache[result['file']].has_key (result['line']):
						id = self.TranslateStacktraceCache[result['file']][result['line']]
				if not id:
					id = session.query( StacktraceTranslated ).filter( StacktraceTranslated.file == result['file'] ).filter( StacktraceTranslated.line == result['line'] ).first()
					if id:
						id = id.id
					else:
						stacktracetranslated = StacktraceTranslated()
						stacktracetranslated.file = result['file']
						stacktracetranslated.line = result['line']
						session.add( stacktracetranslated )
						session.commit()

						if not self.TranslateStacktraceCache.has_key (result['file']):
							self.TranslateStacktraceCache[result['file']] = {}
						self.TranslateStacktraceCache[result['file']][result['line']] = stacktracetranslated.id
						id = stacktracetranslated.id
		return (id)


	def getCacheTranslateStacktrace (self, session, spring, file, address):
		if not self.findSpringModuleFile (file):
			return (None)
		spring = self.dbEncode (spring.strip ())
		file = self.dbEncode (self.findSpringModuleFile (file.strip ()))
		address = self.dbEncode (address.strip ())
		if not spring:
			return (None)

		if self.getCacheTranslateStacktraceCache.has_key (spring):
			if self.getCacheTranslateStacktraceCache[spring].has_key (file):
				if self.getCacheTranslateStacktraceCache[spring][file].has_key (address):
					return (self.getCacheTranslateStacktraceCache[spring][file][address])
		
		id = session.query( CacheStacktrace ).filter( CacheStacktrace.spring == spring ).filter( CacheStacktrace.file == file ).filter( CacheStacktrace.address == address ).first()
		if id:
			if not self.getCacheTranslateStacktraceCache.has_key (spring):
				self.getCacheTranslateStacktraceCache[spring] = {}
				if not self.getCacheTranslateStacktraceCache[spring].has_key (file):
					self.getCacheTranslateStacktraceCache[spring][file] = {}
					if not self.getCacheTranslateStacktraceCache[spring][file].has_key (address):
						self.getCacheTranslateStacktraceCache[spring][file][address] = {'file':id.cppfile, 'line':id.cppline, 'successful':id.successful}
			return ({'file':id.cppfile, 'line':id.cppline, 'successful':id.successful})
		else:
			successful = False
			cppfile = None
			cppline = None
			buildbot = xmlrpclib.ServerProxy('http://springrts.com:8000')
			try:
				result = buildbot.translate_stacktrace ('[      0] ' + spring + ' has crashed.' + '\n' + '[0] (0) ' + file + ' [' + address + ']')
				if len (result) == 1:
					if len (result[0]) == 4:
						cppfile = result[0][2]
						cppline = result[0][3]
						successful = True
			except xmlrpclib.Fault, Error:
				if Error.faultString.index ('Unable to parse detailed version string') != -1:
					successful = False

			cachestacktrace = CacheStacktrace()
			cachestacktrace.spring = spring
			cachestacktrace.file = file
			cachestacktrace.address = address
			cachestacktrace.cppfile = cppfile
			cachestacktrace.cppline = cppline
			cachestacktrace.lastscan = int (time.time())
			cachestacktrace.successful = successful
			session.add( cachestacktrace )
			session.commit()
			return ({'file':cachestacktrace.cppfile, 'line':cachestacktrace.cppline, 'successful':successful})


	###########################################################################################
	# Function which returns the spring file, if available...
	# C:\Program Files\Spring\AI\Skirmish\RAI\0.601\SkirmishAI.dll => \AI\Skirmish\RAI\0.601\SkirmishAI.dll
	#################################################################################
	def findSpringModuleFile (self, line):
		match = self.parseInfologSub ('(\SAI\SSkirmish[^( \()]*)|(\S(spring|spring-hl|spring-mt).exe)', line, 0)
		if match:
			if match.find ('.exe') != -1 or match.find ('.dll') != -1:
				return (match)
		return (None)