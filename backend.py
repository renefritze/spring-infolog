# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import datetime, os

current_db_rev = 5
Base = declarative_base()

class Crash(Base):
	__tablename__ 	= 'records'
	id 				= Column( Integer, primary_key=True,index=True )
	date 			= Column( DateTime )
	extensions		= Column( PickleType )
	settings		= Column( PickleType )
	script			= Column( PickleType )
	filename		= Column( String(255) )

	def __init__(self):
		self.date = datetime.datetime.now()
		
	def basename(self):
		return os.path.basename( self.filename )

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

	def parseZipMembers(self, fn, data ):
		session = self.sessionmaker()
		crash = Crash()
		crash.filename = fn
		session.add( crash )
		session.commit()
		crash_id = crash.id

		if data.has_key( 'ext.txt' ):
			crash.extensions = data['ext.txt'].splitlines()
		if data.has_key( 'script.txt' ):
			crash.script = data['script.txt'].splitlines()
		if data.has_key( 'settings.txt' ):
			crash.settings = zip( map( lambda line: line.split('=')[0], data['settings.txt'].splitlines() ), \
								map( lambda line: line.split('=')[1], data['settings.txt'].splitlines() ) )
				
		#insert actual parsing here
		
		session.add( crash )
		session.commit()
		session.close()
		return crash_id