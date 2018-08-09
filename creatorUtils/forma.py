"""
Formatting package of creatorUtils.
"""

import os;
import hashlib;
import math;
import sys;
import time;
from creatorUtils.compat.types import *;

#Constants
LITTLE = True; # Marker for little endian
BIG = False; # Marker for big endian


##-------------------STRING-------------------##
def hexToStr(inp):
	a = '';
	if math.floor(len(inp)/2.0) != len(inp)/2.0:
		inp = '0' + inp;
	for x in range(len(inp)/2):
		a += chr(int(inp[x * 2:(x * 2) + 2], 16));
	return a;

def numToChars(inp, end = BIG):
	a = hexToStr(numToHex(inp));
	if end:
		a = a[::-1];
	return a;

def pad(inp, num, padding = '0'):
	if not isinstance(padding, stringType):
		raise TypeError('Padding must be a single character string');
	elif len(padding) != 1:
		raise ValueError('Padding must be a single character string');
	if isinstance(inp, str):
		inp = str(inp);
	if (num-len(inp)) <= 0:
		return inp;
	return padding * (num - len(inp)) + inp;


##-------------------NUMBER-------------------##

if sys.version_info[0] < 3:
	def readNum(string, val, end = BIG):
		if len(string) != val:
			raise ValueError('String input must be {} bytes. Got {}'.format(val, len(string)));
		if end:
			a = bytearray(string[::-1]);
		else:
			a = bytearray(string);
		b = 0;
		for x in range(val):
			b = (b << 8) ^ a[x];
		return b;
else:
	def readNum(string, val, end = BIG):
		if not isinstance(string, bytes):
			raise TypeError('`string` MUST be an instance of bytes');
		if len(string) != val:
			raise ValueError('String input must be {} bytes. Got {}'.format(val, len(string)));
		if end:
			a = string[::-1];
		else:
			a = string;
		b = 0;
		for x in range(val):
			b = (b << 8) ^ a[x];
		return b;

def readInt(string, end):
	a = '<' if end else '>';
	struct.unpack('{}I'.format(a), string)

def readLong(string, end):
	a = '<' if end else '>';
	struct.unpack('{}Q'.format(a), string)

def readShort(string, end):
	a = '<' if end else '>';
	struct.unpack('{}H'.format(a), string)

##-------------------HEXADECIMAL-------------------##
def strToHex(s, encoding = None):
	if encoding:
		s = s.encode(encoding);
	return ''.join('{:02x}'.format(ord(c)) for c in s);

def numToHex(inp):
	out = '{:x}'.format(inp);
	if len(out) % 2 != 0:
		out = '0' + out;
	return out;

def toHex(inp, encoding = None):
	"""
	Converts many data types into a hexadecimal value. Value is not
	prepended with "0x", but it is prepended with a single "0" if the
	length is not a multiple of two. If encoding is specified, it will
	only be used if needed Input type matters as it determines what
	function will be used to convert it. The table bellow shows how the
	function is determined.
	 + String:  \tforma.strToHex
	 + Unicode: \tforma.strToHex
	 + Long:    \tforma.numToHex
	 + int:     \tforma.numToHex
	"""
	if isinstance(inp, stringType):
		return strToHex(inp);
	if isinstance(inp, intlong):
		return numToHex(inp);
	raise TypeError('Input must be an integer, long, string, or unicode.');

def msgEpoch(inp):
	ep = 116444736000000000;
	inp = ''.join(inp.split(' '));
	inp2 = '';
	for x in range(len(inp)/2):
		inp2 = inp[2 * x: (2 * x) + 2] + inp2;
	print(inp2);
	inp = int(inp2, 16);
	return (inp - ep)/10000;

##-------------------HASHES-------------------##
## NOTE:	These hash functions are provided as shorthands for getting
##			the hex digest of a string.
def md5(inp):
	return hashlib.md5(inp).hexdigest();

def sha256(inp):
	return hashlib.sha256(inp).hexdigest();

def sha1(inp):
	return hashlib.sha1(inp).hexdigest();

def sha512(inp):
	return hashlib.sha512(inp).hexdigest();

##-------------------ENDIENNESS-------------------##
def changeBitEndianness(inp):
	"""
	Switches the bit endienness of a single character.
	"""
	a = bin(ord(inp));
	a = pad(a[2:], 8)[::-1];
	return chr(int(a, 2));

def changeByteEndianness(inp):
	"""
	Takes the input string and returns the reverse,
	effectively switching the endienness.
	"""
	return inp[::-1];

changeBitEndian = changeBitEndianness;
changeByteEndian = changeByteEndianness;
