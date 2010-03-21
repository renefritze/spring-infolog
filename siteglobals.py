# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
from backend import Backend
from ConfigParser import SafeConfigParser as ConfigParser
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

class SimpleConfig(ConfigParser):
	def __init__(s,fn='site.cfg'):
		ConfigParser.__init__( s )
		s.read(fn)
		if not s.has_section('site'):
			s.add_section('site')
			
config = SimpleConfig()
db = Backend( config.get('db', 'alchemy-uri') )

cache_opts = {
    'cache.type': 		config.get('cache','type'),
    'cache.data_dir':	config.get('cache','data_dir'),
    'cache.lock_dir': 	config.get('cache','lock_dir')
}

env = Environment(loader=FileSystemLoader('templates'))
cache = CacheManager(**parse_cache_config_options(cache_opts))
