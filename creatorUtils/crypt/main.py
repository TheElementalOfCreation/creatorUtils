import math;
import random;
import os;
from os import path as Path;
import sys;
from creatorUtils.compat import progress_bar;

if sys.version_info[0] < 3:
	req = raw_input;
else:
	req = input;

alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

def bxor(inp, key):
	"""
	Preforms the bitwise xor on a full string.
	"""
	inp = bytearray(inp);
	key = bytearray(key)
	return str(bytearray([inp[i] ^ key[i % len(key)] for i in range(len(inp))]));

def string(data, key):
	"""
	Encrypts the string "data" with "key".
	"""
	return bxor(data, randXOR(data, key));

def randXOR(data, key, r = None, start = 0):
	"""
	"Random" masking function. "r" must be an instance of
	random.Random
	"""
	dlen = len(data);
	if r == None:
		r = random.Random(key);
	key1 = bytearray((key[start:] + (key * int(math.ceil((dlen / float(len(key)))))))[0:len(data)]);
	data = bytearray(data);
	return str(bytearray([data[i] ^ key1[i] ^ r.randint(0, 255) for i in range(dlen)]));

def randStr(length):
	"""
	Generates a string of random letters with a
	length equal to "length".
	"""
	a = '';
	while len(a) < length:
		a += alpha[int(math.floor(random.random() * 52)) % 52];
	return a;

def file(path1, key, pagesize = 262144, rand = True, overwrite = False):
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
	if pagesize < 1024:
		raise Exception('pagesize MUST be at least 1024 for stability');
	#if pagesize > 4096:
	if pagesize > 100000000:
		print('WARNING: Page size is above the max stable limit.\nDo you want to continue?');
		if req('"Y"/"N" (Case Sensitive!): ') != 'Y':
			print('Stopping...');
			return;
	try:
		file1 = open(path1, 'rb');
		while True:
			nm = randStr(9);
			if nm not in os.listdir('.'):
				break;
		file2 = open(nm, 'wb');
		fsize = int(math.ceil(Path.getsize(path1)/float(pagesize)));
		probar = progress_bar.ProgressBar();
		start = 0;
		r = random.Random(key);
		if rand:
			for x in probar(range(fsize)):
				file2.write(randXOR(file1.read(pagesize), key, r, start));
				file2.flush();
				start = (start + pagesize) % len(key);
		else:
			for x in probar(range(fsize)):
				file2.write(bxor(file1.read(pagesize), key, start));
				file2.flush();
		file1.close();
		file2.close();
		assert(Path.getsize(path1) == Path.getsize(nm));
		if overwrite:
			os.remove(path1);
			os.rename(nm, path1);
		else:
			os.rename(nm, path1 + '.crypt');
	except:
		try:
			file1.close();
		except:
			pass;
		raise;
