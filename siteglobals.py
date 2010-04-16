# -*- coding: utf-8 -*-
from __future__ import with_statement
from jinja2 import Environment, FileSystemLoader
from backend import Backend
from ConfigParser import SafeConfigParser as ConfigParser
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import tasbot

class SimpleConfig(ConfigParser):
	tasbot_cfg_filename = '.tasbot.cfg'
	def __init__(s,fn='site.cfg'):
		ConfigParser.__init__( s )
		s.read(fn)
		if not s.has_section('site'):
			s.add_section('site')
		assert s.has_section('tasbot'), 'You need to have a tasbot section in your config file, see site.cfg.example'
		with open(SimpleConfig.tasbot_cfg_filename, 'w') as tasbot_cfg:
			for (name,val) in s.items('tasbot'):
				tasbot_cfg.write( '%s=%s;\n'%(name,val) )
			
config = SimpleConfig()
db = Backend( config.get('db', 'alchemy-uri') )

cache_opts = {
    'cache.type': 		config.get('cache','type'),
    'cache.data_dir':	config.get('cache','data_dir'),
    'cache.lock_dir': 	config.get('cache','lock_dir')
}

is_debug = config.getboolean('site','debug')
env = Environment(loader=FileSystemLoader('templates'))
cache = CacheManager(**parse_cache_config_options(cache_opts))
tasbot = tasbot.bot()
tasbot.run(SimpleConfig.tasbot_cfg_filename,False,True)
