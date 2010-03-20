# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import backend
from ConfigParser import SafeConfigParser as ConfigParser
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'memory',
    'cache.data_dir': 'tmp/cache/data',
    'cache.lock_dir': 'tmp/cache/lock'
}

class SimpleConfig(ConfigParser):
	def __init__(s,fn='site.cfg'):
		ConfigParser.__init__( s )
		s.read(fn)
		if not s.has_section('site'):
			s.add_section('site')
			
config = SimpleConfig()
#db = backend.Db( config.get('', 'alchemy-uri') )
env = Environment(loader=FileSystemLoader('templates'))
cache = CacheManager(**parse_cache_config_options(cache_opts))
