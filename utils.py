# -*- coding: utf-8 -*-

class DummyException:
	"""usable as stand-in when one want to disable excp catching"""
	pass

def unicodeField( field ):
	return unicode(field, 'latin-1', 'replace')

def getFieldsByPrefix( prefix, request ):
	filtered = dict()
	for k in request.GET.keys():
		if k.startswith( prefix ):
			filtered[k] = unicodeField(request.GET[k])
	return filtered

def getAllFields( prefix, request ):
	filtered = dict()
	for k in request.GET.keys():
		filtered[k] = unicodeField(request.GET[key])
	return filtered

def getSingleField( key, request, default=None ):
	if key in request.GET.keys():
		return unicodeField(request.GET[key])
	else:
		return default

def getSingleFieldPOST( key, request, default=None ):
	if key in request.POST.keys():
		return unicodeField(request.POST[key])
	else:
		return default

def getFieldsByPrefixPOST( prefix, request ):
	filtered = dict()
	for k in request.POST.keys():
		if k.startswith( prefix ):
			filtered[k] = request.POST[k]
	return filtered

def SortAsc( condition, ascending = 'True' ):
	if ascending == 'True':
		return condition.asc()
	else:
		return condition.desc()
