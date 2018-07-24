import os;
import os.path;
import struct;
from creatorUtils.compat.types import *;

def bufferedWrite(outfile, infile, pagesize, length):
	a = length/pagesize;
	b = (length - (pagesize * a));
	for x in range(a):
		r = infile.read(pagesize);
		if len(r) != pagesize:
			raise EOFError('Length of data read differs from expected length. Expected {}, got {}'.format(pagesize, len(r)));
		outfile.write(r);
		outfile.flush();
	r = infile.read(b);
	if len(r) != b:
		raise EOFError('Length of data read differs from expected length. Expected {}, got {}'.format(b, len(r)));
	outfile.write(r);
	outfile.flush();

class DotNumParser(object):
	"""
	Parser for a special "dotnum" archive file type.
	Specification is as follows:
		+ File extension is a single digit (Ex: helloworld.3)
		+ Contains a header that starts with a single unsigned
			little-endian integer (abbreviated as ULEI). That
			ULEI specifies how many unsigned ULEIs will follow.
			Each ULEI after this one should be added at a table.
		+ Each following ULEI will specify the length of a file.
			After the header is read, starting at the first ULEI
			in the table, that many bytes should be read. Those
			bytes are a file.
	"""
	def __init__(self, fileName = None):
		object.__init__(self);
		self.__entries = None;
		self.__fileName = None;
		self.__File = None;
		if fileName != None:
			self.open(fileName);

	def __open(self):
		self.__position = 0;
		if self.__File != None:
			self.close();
		self.__File = open(self.__fileName, 'rb');
		self.__readHead();

	def __readHead(self):
		if self.__position != 0:
			raise Exception('__readHead called when position is not 0!');
		self.__head = [];
		i = self.__readNextInt();
		self.__entries = i + 1;
		for x in range(i):
			self.__head.append(self.__readNextInt());

	def __readNextInt(self):
		"""
		Reads integer in little endian byte format and big endian bit format.
		"""
		a = self.__File.read(4);
		if len(a) != 4:
			raise EOFError('Length of data read differs from expected length. Expected {}, got {}'.format(4, len(a)));
		integer = struct.unpack('<I', a)[0];
		self.__position += 4;
		return integer;

	#Public methods#
	def close(self):
		if self.__File != None:
			try:
				self.__File.close();
				self.__File = None;
			except:
				self.__File = None;

	def open(self, fileName):
		self.__fileName = fileName;
		self.__open();

	def save(self, pagesize = 0xffff, saveFolder = None):
		origin = os.getcwd();
		if saveFolder == None:
			saveFolder = self.__fileName + ' extracted';
		try:
			os.mkdir(saveFolder);
		except:
			pass;
		os.chdir(saveFolder);
		for x in range(len(self.__head)):
			file1 = open(str(x), 'wb');
			bufferedWrite(file1, self.__File, pagesize, x);
			file1.close();
		os.chdir(origin);
		self.__File.seek(self.__position);

	@property
	def head(self):
		return self.__head;



class DotNumGenerator(object):
	"""
	Generator class for dotnum file type.

	Note: Files must be less than or equal to 4294967295
	bytes (~4 GB) ((2^32) - 1) in length.
	"""
	def __init__(self):
		object.__init__(self);
		self.__numberOfFiles = 0;
		self.__Files = [];

	def addFileByData(self, data, pos = None):
		data = binString(data);
		if pos == None:
			self.__Files.append(('DATA', data));
		else:
			self.__Files.insert(pos, ('DATA', data));
		self.__numberOfFiles += 1;

	def addFileByName(self, name, pos = None):
		if pos == None:
			self.__Files.append(('NAME', name));
		else:
			self.__Files.insert(pos, ('NAME', name));
		self.__numberOfFiles += 1;

	def addFileByFile(self, fileObj, pos = None):
		if not fileObj.closed and fileObj.mode == 'rb':
			fileObj.seek(0);
			if pos == None:
				self.__Files.append(('FILE', fileObj));
			else:
				self.__Files.insert(pos, ('FILE', fileobj))
		else:
			if fileObj.closed:
				raise Exception('File object is closed.');
			else:
				raise Exception('File object must be opened in binary read mode');

	def save(self, name, pagesize = 0xffff):
		"""
		Saves the files into a dotnum file.
		`pagesize` controls the size of the write buffer.
		"""
		lens = [self.__numberOfFiles];
		for x in range(self.__numberOfFiles):
			a = self.__Files[x];
			if a[0] == 'DATA':
				b = len(a[1]);
			elif a[0] == 'NAME':
				b = os.path.getsize(path);
			elif a[0] == 'FILE':
				a[1].seek(0, 2);
				b = a[1].tell();
				a[1].seek(0);
			if b > 0xffffffff:
				raise Exception('File {} is too large ({} bytes, which is {} too many).'.format(x, b, b-0xffffffff));
			lens.append(b);
		#We will only end up here if no errors have occured
		f = open(name, 'wb');
		for x in range(len(lens)):
			f.write(struct.pack('<I', lens[x]));
			f.flush();
		for x in range(self.__numberOfFiles):
			a = self.__Files[x];
			if a[0] == 'DATA':
				f.write(a[1]);
				f.flush();
			elif a[0] == 'NAME':
				fi = open(a[1], 'rb');
				bufferedWrite(f, fi, pagesize, lens[x + 1]);
				fi.close();
			elif a[0] == 'FILE':
				bufferedWrite(f, a[1], pagesize, lens[x + 1]);
		f.close();
