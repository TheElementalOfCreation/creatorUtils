from json import *;
import sys;

"""
Library for Python 2 (with python 3 compatibility)
for forcing string objects instead of unicode ones
in json dumping and loading.

Byteify based functions from:
https://stackoverflow.com/a/33571117/7723054
"""

if sys.version_info[0] < 3:
	def json_load_byteified(file_handle):
		return _byteify(
			load(file_handle, object_hook=_byteify),
			ignore_dicts=True
		);

	def json_loads_byteified(json_text):
		return _byteify(
			loads(json_text, object_hook=_byteify),
			ignore_dicts=True
		);

	def _byteify(data, ignore_dicts = False):
		# if this is a unicode string, return its string representation
		if isinstance(data, unicode):
			return data.encode('utf-8');
		# if this is a list of values, return list of byteified values
		if isinstance(data, list):
			return [ _byteify(item, ignore_dicts=True) for item in data ];
		# if this is a dictionary, return dictionary of byteified keys and values
		# but only if we haven't already byteified it
		if isinstance(data, dict) and not ignore_dicts:
			return {
				_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
				for key, value in data.iteritems()
			};
		# if it's anything else, return it in its original form
		return data;

	def dumpsStr(*args, **kwargs):
			if 'encoding'not in kwargs:
				kwargs['encoding'] = 'iso-8859-1';
			return dumps(*args, **kwargs);

	def dumpStr(*args, **kwargs):
			if 'encoding'not in kwargs:
				kwargs['encoding'] = 'iso-8859-1';
			return dump(*args, **kwargs);

	loadsStr = json_loads_byteified;
	loadStr = json_load_byteified;
else:
	loadsStr = loads;
	loadStr = load;
	dumpsStr = dumps;
	dumpStr = dump;
