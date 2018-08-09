"""
Module used to define variables that work to check if
a variable is a type of string or if it is an int or
long. This module makes it so that the functions will
not fail if using Python 3. Needed for many of my
scrits.

To check if a variable is a string or unicode
(or just a string in Python 3), use:

	`type(var) in stringType`
			or
	`isinstance(var, stringType)`

to check if a variable is an integer or long (or just
an integer in Python 3) use:

	`type(var) in intlong`
			or
	`isinstance(var, intlong)`
"""

import sys

if sys.version_info[0] < 3:
	stringType = [str, unicode];
	intlong = [int, long];
	bytes = bytearray;
else:
	stringType = [str];
	intlong = [int];
	import io;
	file = io.IOBase;

def a():
	pass;

function = a.__class__;
builtin_function = hex.__class__;
