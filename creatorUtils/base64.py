import base64;
import string;

DEFAULT_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def b64decode(s, altchars = {}):
	if isinstance(altchars, dict):
		altchars = (''.join(altchars.keys()), ''.join(altchars.values()));
	s = s.translate(string.maketrans(*altchars[::-1]));
	return base64.b64decode(s);

def b64encode(s, altchars = None):
	if isinstance(altchars, dict):
		altchars = (''.join(altchars.keys()), ''.join(altchars.values()));
	s = base64.b64encode(s);
	return s.translate(string.maketrans(*altchars));
