import os;
from creatorUtils.compat.types import *;
from creatorUtils.compat import progress_bar as pb;


if os.name == 'nt':
	from ctypes import wintypes, windll, create_unicode_buffer;
	_GetShortPathNameW = windll.kernel32.GetShortPathNameW;
	_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD];
	_GetShortPathNameW.restype = wintypes.DWORD;

	def get_long_path_name(input):
		"""
		Returns the long path name of a file or directory.
		"""
		BUFFER_SIZE = 500;
		buffer = create_unicode_buffer(BUFFER_SIZE);
		windll.kernel32.GetLongPathNameW(input, buffer, BUFFER_SIZE);
		return buffer.value;

	def get_short_path_name(long_name):
		"""
		Gets the short path name of a given long path.
		http://stackoverflow.com/a/23598461/200291
		"""
		output_buf_size = 0;
		while True:
			output_buf = create_unicode_buffer(output_buf_size);
			needed = _GetShortPathNameW(long_name, output_buf, output_buf_size);
			if output_buf_size >= needed:
				return output_buf.value;
			else:
				output_buf_size = needed;

else:
	def get_long_path_name(input):
		return input;

	def get_short_path_name(input):
		return input;

def getall(inp, specExt = True, ext = ['msg'], extsep = '.', progressBar = None, onerror = None):
	"""
	Return format:
		PathTable, NameTable, outPath
	Returns a list of the paths of all of the files in
	a directory and a list of the filenames. If the
	input is a file instead of a directroy it will
	return the path and filename of just that file.
	The arguments are as follows:
	> `inp`:			The input folder or file.
	> `scepExt`:		Boolean. Tells the function if you are ONLY looking for files
						with the extension "ext".
	> `ext`:			The specific extension that a file must have is scepExt is True.
	> `extsep`:			Specifies the seperator between filename and extension.
	> `progressBar`:	Specifies the progress bar to use. Should either be None or a
						progressbar instance.
	> `onerror`:		Function to be passed to the `onerror` argument of `os.walk`.
	"""
	if type(ext) in stringType:
		ext = [ext];
	if isinstance(ext, tuple):
		ext = list(ext);
	if not isinstance(ext, list):
		raise TypeError('Input "ext" must be a list, tuple, or string');
	for x in range(len(ext)):
		ext[x] = ext[x].lower(); #Change the input extension to all lowercase letters
	inp = get_long_path_name(get_short_path_name(os.path.abspath(inp)));
	inp = inp.replace('\\','/'); #Replaces every "\" in a path with a "/".
	a = [];
	c = [];
	v = os.walk(inp, onerror = onerror);
	if progressBar == None:
		progressBar = pb.ProgressBar();
	iterator = progressBar(v);
	isfile = True;
	try:
		while True:
			current = iterator.next();
			isfile = False;
			for x in current[2]:
				if not specExt or x.split(extsep).pop().lower() in ext:
					entry = current[0].replace('\\', '/') + '/' + x;
					a.append(entry);
					c.append(x);
	except StopIteration:
		if isfile:
			if inp.split(extsep).pop().lower() in ext:
				a.append(inp);
				c.append(extsep.join(inp.split('/')[-1].split(extsep)[:-1]));
	outPath = '/'.join(inp.split('/')[:-1]);
	return a, c, outPath;

def delFolder(path = None, top = True):
	"""
	Deletes the folder at the specidied path along
	with it's contents. The entire thing is wrapped
	inside of a try loop so that it can properly
	display error messages so they can be reported.
	"""
	lowest = True;
	try:
		if path == None:
			return;
		a, b, unneeded = getall(path, False);
		for fil in a:
			os.remove(get_short_path_name(fil));
		try:
			os.rmdir(path);
		except Exception as err:
			if len(os.listdir(path)) == 0:
				raise err;
			for x in os.listdir(path):
				lowest = False;
				delFolder(path + '/' + x, False);
				lowest = True;
			os.rmdir(path);
	except Exception as err:
		if lowest:
			print('An Exception has occured!');
			print('If this is the first time you are seeing this, ignore it and try again.');
			print('If this error continues to happen, please report the following data:');
		print(err);
		print('Path: ' + path);
		if top == False:
			raise Exception('Exception occured within sub-call of command:');
		s = input();

def isFile(inp):
	"""
	Returns True if the input is a file.
	Returns False if the input is a directory.
	Raises an Exception if the path does not exist.
	"""
	if os.path.exists(inp):
		return os.path.isfile(inp);
	else:
		raise OSError('Cannot find the path specified: "{}"'.format(inp));

def isFolder(inp):
	"""
	Returns False if the input is a file.
	Returns True if the input is a directory.
	Raises an Exception if the path does not exist.
	"""
	if os.path.exists(inp):
		return os.path.isdir(inp);
	else:
		raise OSError('Cannot find the path specified: "{}"'.format(inp));

def split(inp):
	"""
	Like os.path.split, but splits at EVERY backslash and fowardslash.
	"""
	return tuple(inp.replace('\\', '/').split('/'));

#def getallFolders():
