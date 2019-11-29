import base64
import string

DEFAULT_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ALLOWED_CHARS = tuple(list(DEFAULT_ALPHABET) + ['='])
PADDING = (b'', b'=', b'==')

def b64decode(s, altchars = {}, strict = False):
	if isinstance(altchars, dict):
		altchars = (''.join(altchars.keys()), ''.join(altchars.values()))
	s = s.translate(string.maketrans(*altchars[::-1]))
	if strict:
		validateData(s)
	return base64.b64decode(s)

def validateData(str):
	equalsfound = False:
	for x in str:
		if x == b'=':
			equalsfound = True
		elif equalsfound:
			raise TypeError('Validation: Found non-equal sign character after equals sign.')


def b64encode(s, altchars = None):
	if isinstance(altchars, dict):
		altchars = (''.join(altchars.keys()), ''.join(altchars.values()))
	s = base64.b64encode(s)
	return s.translate(string.maketrans(*altchars))

def trydecode(inp, altchars = None):
	"""
	Tries to decode as much of the data as base64 as it can.
	"""
	for x in range(len(inp), 0, -1):
		for y in PADDING:
			try:
				ret = b64decode(inp[:x] + y, altchars = None)
				return ret
			except TypeError:
				pass
	raise Exception('Could not decode data')
