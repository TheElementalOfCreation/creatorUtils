"""
Module used to define variables that work to check if
a variable is a type of string or if it is an int or
long. This module makes it so that the functions will
not fail if using Python 3. Needed for many of my
scrits.

To check if a variable is a string or unicode
(or just a string in Python 3), use:
	`type(var) in stringType`

to check if a variable is an integer or long (or just
an integer in Python 3) use:

	`type(var) in intlong`

To make a string into a value that can be succesfully
written to a binary file every time, use:
	`binaryString(var)`
"""

import sys

if sys.version_info[0] < 3:
	stringType = [str, unicode];
	intlong = [int, long];
	def binString(inp):
		if isinstance(inp, unicode):
			try:
				return inp.encode('latin-1');
			except:
				return inp.encode('utf-8');
		else:
			return inp.decode('latin-1').encode('latin-1');
else:
	stringType = [str];
	intlong = [int];
	bytearray = bytes;
	import io;
	file = io.IOBase;
	def binString(inp):
		if isinstance(inp, bytes):
			return inp;
		else:
			try:
				return inp.encode('latin-1');
			except:
				return inp.encode('utf-8');

function = binString.__class__;
builtin_function = hex.__class__;
