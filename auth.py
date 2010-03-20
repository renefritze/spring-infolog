# -*- coding: utf-8 -*-
import bottle
import hashlib
import time
import base64
import random
from db_entities import Roles, Player
try:
    import json
except ImportError:
    import simplejson as json 


# copied and adjusted from helper class in torque( http://github.com/jreid42/torque )

class AuthDecorator(object):
	def __init__(self,role,db):
		self.role = role
		self.db = db

	def _parseBasicAuth(self,authorization_header):
		try:
			authScheme, credentials = authorization_header.split(' ')
		except:
			return None, None

		if authScheme == 'Basic':
			try:
				username,password = base64.b64decode(credentials).split(':')
			except Exception, e:
				print e
				return None, None
			else:
				return username,password
		else:
			return None, None

	def _401Response(self,msg="You need to authenticate with our servers before you may access this content."):
		bottle.response.status = 401
		bottle.response.set_content_type('text/json')
		#log.info('401 Response Returned: '+msg)

		bottle.response.header['WWW-Authenticate'] = 'Basic realm="SpringLadder"'
		return json.dumps({"success": False,"msg": msg})

	def __call__(self,f):
		def wrapped(*args,**kwargs):
			if 'HTTP_AUTHORIZATION' not in bottle.request.environ:
				return self._401Response()

			header = bottle.request.environ['HTTP_AUTHORIZATION']
			username,password = self._parseBasicAuth(header)
			if (username == None) | (password == None):
				return self._401Response()

			session = self.db.sessionmaker()
			try:
				player = self.db.GetPlayer(username)
			except:
				return self._401Response(msg='Username and password combination is invalid.')
			else:
				if not player.validate(password):
					return self._401Response(msg='Username and password combination is invalid.')

				ok = self.db.AccessCheck( -1, username, self.role )
				if not ok:
					return self._401Response(msg='User does not have the correct permissions.')

				setattr(bottle.request,'player',player)
				return f(*args,**kwargs)

		return wrapped