import hashlib;
import math;
import os;
import random;
import sys;
from creatorUtils.compat import progress_bar;
from creatorUtils.compat import structures;
from creatorUtils.compat.types import *;

def create_hash(name, data):
	HASH_FUNCTIONS[name][0](*HASH_FUNCTIONS[name], data);

alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

def insecure(algorithm):
	print('WARNING: Selected method "' + algorithm + '" is considered to be insecure. Use at your own risk.');

def secure(algorithm):
	pass;

def unknown(algorithm):
	print('WARNING: Unrecognized algorithm "' + algorithm + '". It may be insecure.');

def hashlib_hash_functions(method, data):
	return hashlib.new(method, data).digest()

# Define Constants
MD4 = 'MD4';
MD5 = 'MD5';
SHA1 = 'SHA1';
SHA224 = 'SHA224';
SHA256 = 'SHA256';
SHA384 = 'SHA384';
SHA512 = 'SHA512';
WHIRLPOOL = 'whirlpool';

HASH_METHODS = [
	MD4,
	MD5,
	SHA1,
	SHA224,
	SHA256,
	SHA384,
	SHA512,
	WHIRLPOOL,
];

HASH_METHOD_WARNING = {
	MD4: insecure,
	MD5: secure,
	SHA1: secure,
	SHA224: secure,
	SHA256: secure,
	SHA384: secure,
	SHA512: secure,
	WHIRLPOOL: secure,
};

HASH_FUNCTIONS = {
	MD4: (hashlib_hash_functions, (MD4,)),
	MD5: (hashlib_hash_functions, (MD5,)),
	SHA1: (hashlib_hash_functions, (SHA1,)),
	SHA224: (hashlib_hash_functions, (SHA224,)),
	SHA256: (hashlib_hash_functions, (SHA256,)),
	SHA384: (hashlib_hash_functions, (SHA384,)),
	SHA512: (hashlib_hash_functions, (SHA512,)),
	WHIRLPOOL: (hashlib_hash_functions, (WHIRLPOOL,)),
};

def randStr(length):
	"""
	Generates a string of random letters with a
	length equal to "length".
	"""
	a = '';
	while len(a) < length:
		a += alpha[int(math.floor(random.random() * 52)) % 52];
	return a;

class HashDataGenerator(object):
	"""
	EMPTY
	"""
	def __init__(self, string_or_bytes, encoding = None, methods = [SHA512]):
		object.__init__(self);
		for x in methods:
			HASH_METHOD_WARNING.get(x, unknown)(x);
		self.__originalData = string_or_bytes if isinstance(string_or_bytes, bytes) else bytes(string_or_bytes, encoding = encoding);
		self.__method = structures.repeater(methods);
		self.__currentData = bytes(hashlib.new(self.__method(), self.__originalData).digest());
		self.__position = 0;

	def gen(self, length):
		a = bytes(b'');
		g = len(self.__currentData) - self.__position;
		a += self.__currentData[self.__position:self.__position + g];
		remaining = length - len(a);
		while remaining:
			self.__currentData = bytes(create_hash(self.__method(), self.__currentData));
			curlen = len(self.__currentData);
			if remaining <= curlen:
				self.__position = remaining;
				a += self.__currentData[:remaining];
				remaining = 0;
			else:
				a += self.__currentData;
				remaining -= curlen;
		return a;

	def reset(self):
		self.__position = 0;
		self.__method.reset();
		self.__currentData = self.__originalData;


if sys.version_info[0] < 3:
	req = raw_input;
else:
	req = input;

def bxor(inp, key):
	"""
	Preforms the bitwise xor on an array of bytes.
	"""
	return bytes([inp[i] ^ key[i % len(key)] for i in range(len(inp))]);

def crypt_string(data, key, encoding):
	"""
	Encrypts the string `data` with `key`.
	Both should be a string with the same encoding.

	Returns a bytes object.
	"""
	return randXOR(bytes(data, encoding), bytes(key, encoding));

def crypt_bytes(data, key):
	"""
	Encrypts the bytearray `data` with the bytearray `key`
	"""
	return randXOR(data, key);

def randXOR(data, key, r = None, start = 0):
	"""
	"Random" masking function. `r` must be an instance of
	HashDataGenerator.
	"""
	if not isinstance(data, bytes):
		raise TypeError('All data inputs must be bytes.')
	dlen = len(data);
	if r == None:
		r = HashDataGenerator(key);
	key1 = bytes((key[start:] + (key * int(math.ceil((dlen / float(len(key)))))))[:len(data)]);
	data = data;
	rand = r.gen(dlen);
	return bytes([data[i] ^ key1[i] ^ rand[i] for i in range(dlen)]);


def crypt_file(path1, key, pagesize = 262144, rand = True, overwrite = False, hash_methods = [SHA512, SHA256, MD5, WHIRLPOOL]):
	"""
	Function to encrypt whole files.
	 +	"path1" is the path to the file to be encrypted.
	 +	"key" is the encyprtion key being used.
	 +	"pagesize" is the number of bytes read at a time. Setting this
			Value too high or too low will make the program a lot slower.
			The recommended size is 262144.
	 +	"rand" is the switch for whether the program should use the
	 		random-modified key, which is much more secure. Setting
			this to True will turn this on (slower, more secure)
	 + "overwrite" is the option the determines if the original file
	 		will be overwritten. Setting this to False will cause the
			function to write to the file "(filename).crypt".
	"""
	pagesize = int(pagesize);
	key = bytes(key);
	if pagesize < 1024:
		raise Exception('pagesize MUST be at least 1024 for stability');
	#if pagesize > 4096:
	if pagesize > 100000000:
		print('WARNING: Page size is above the max stable limit.\nDo you want to continue?');
		if req('"Y"/"N" (Case Sensitive!): ') != 'Y':
			print('Stopping...');
			return;
	with open(path1, 'rb') as file1:
		while True:
			nm = randStr(9);
			if nm not in os.listdir('.'):
				break;
		with open(nm, 'wb') as file2:
			fsize = int(math.ceil(os.path.getsize(path1)/float(pagesize)));
			probar = progress_bar.ProgressBar();
			start = 0;
			r = HashDataGenerator(key, methods = hash_methods);
			if rand:
				for x in probar(range(fsize)):
					file2.write(randXOR(bytes(file1.read(pagesize)), key, r, start));
					file2.flush();
					start = (start + pagesize) % len(key);
			else:
				for x in probar(range(fsize)):
					file2.write(bxor(bytes(file1.read(pagesize)), key, start));
					file2.flush();
	assert(os.path.getsize(path1) == os.path.getsize(nm));
	if overwrite:
		os.remove(path1);
		os.rename(nm, path1);
	else:
		os.rename(nm, path1 + '.crypt');



def add_new_hash_method(name, security, hash_function, args):
	"""
	Use to define a new type of hash function. Provide the name,
	one of the security functions (secure, insecure, unknown),
	the function to do the hash, and any arguments that come
	before the data input.
	"""
	if not isinstance(name, stringType):
		raise TypeError('Name must be a string.');
	if len(name) == 0:
		raise ValueError('Name must be at least one character long.');
	if not isinstance(security, functionType):

	# No issues with the inputs themselves
	if name in HASH_METHODS:
		raise Exception('Method already exists: '+ name);

	# Seems to be valid, and does not already exist
	HASH_METHODS.append(name);
	HASH_METHOD_WARNING[name] = security;
	HASH_FUNCTIONS[name] = (hash_function, tuple(args));
