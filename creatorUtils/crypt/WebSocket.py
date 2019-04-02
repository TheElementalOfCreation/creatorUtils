import base64;
import gc;
import hashlib;
import zlib;
import struct;
#TODO#TODO MAJOR modifications to the way the code works so that it will handle unicode and stuff properly. Also it will use struct for packing and unpacking some things
from creatorUtils import forma;
from creatorUtils.compat.types import *;

def unmask(data):
	data = bytes(data);
	toRead = 0;
	remaining = bytes(b'');
	masked = 128 == (data[1] & 128);
	datalen = (0x7F & data[1]);
	if datalen == 126:
		x = 4;
		toRead = struct.unpack('>H', data[2:4])[0];
	elif datalen == 127:
		x = 10;
		toRead = struct.unpack('>Q', data[2:10])[0];
	else:
		x = 2;
		toRead = datalen;
	if masked:
		str_data = '';
		if datalen > 0:
			mask_key = data[x:x+4];
			masked_data = data[x+4:x+4+toRead];
			unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))];
			str_data = bytes(unmasked_data);
			remaining = data[x+4+toRead:];
	else:
		str_data = bytes(data)[x:x+toRead];
		remaining = data[x+toRead:];
	return str_data, remaining;


def mask(data, key = b'', byte = 0b10000010):
	"""
	`byte` is the first byte. This defaults to "0b10000010"
	which would make the function generate it. Doing
	this allows for much more message control for
	functions calling this one. For example, this
	allows a function to pass the data to this function
	in chunks. If the most significant bit is `a` and
	the least significant bit is `h`, the bits can be
	labeled as follows:

			`abcdefgh`

	where `a` signifies that this frame is the last
	part of a message being sent, `b`, `c`, and `d`
	are reserved and MUST be zero unless an extention
	has been negotiated that says otherwise, and `efgh`
	signifies the data type.

	The following is a list of possible datatypes:
	 + 0b0000 = Continuation
	 + 0b0001 = Text
	 + 0b0010 = Binary
	 + 0b0011 = Reserved for further non-control frames
	 + 0b0100 = Reserved for further non-control frames
	 + 0b0101 = Reserved for further non-control frames
	 + 0b0110 = Reserved for further non-control frames
	 + 0b0111 = Reserved for further non-control frames
	 + 0b1000 = Connection Close
	 + 0b1001 = Ping
	 + 0b1010 = Pong
	 + 0b1011 = Reserved for further control frames
	 + 0b1100 = Reserved for further control frames
	 + 0b1101 = Reserved for further control frames
	 + 0b1110 = Reserved for further control frames
	 + 0b1111 = Reserved for further control frames
	"""
	if len(key) > 0 and len(key) != 4:
		raise Exception('Key must be 4 or 0 bytes.');
	datalen = len(data);
	ad = '';
	if datalen > 125:
		if datalen > 0xffff:
			ad = forma.pad(forma.numToChars(datalen), 8, '\x00');
			if len(ad) != 8:
				raise Exception('Data is too long ({0} bytes)'.format(datalen));
			datalen = 127;
		else:
			ad = forma.pad(forma.numToChars(datalen), 2, '\x00');
			datalen = 126;
	if len(key) > 0:
		str_data = bytes([byte, 128 + datalen] + list(bytes(ad)) + list(bytes(key)));
	else:
		str_data = chr(byte) + chr(datalen) + ad + str(key);
	if datalen > 0:
		if len(key) > 0:
			mask_key = bytes(key);
			unmasked_data = bytes(data);
			masked_data = [unmasked_data[i] ^ mask_key[i%4] for i in range(len(unmasked_data))];
			str_data += bytes(masked_data);
		else:
			str_data += bytes(data);
	return str_data;

def limitedMask(data, key = b'1y6S', max = 1000, type = 2):
	type = type & 15;
	if max % 4 != 0:
		raise ValueError('`max` must be a multiple of 4');
	datatable = [];
	pos = 0;
	if len(data) - pos > max:
		datatable.append(mask(data[pos:pos + max], key, type));
		pos += max;
	else:
		datatable.append(mask(data[pos:pos + max], key, 128 | type));
	while len(data) - pos > max:
		datatable.append(mask(data[pos:pos + max], key, type & 240));
		pos += max;
	if pos != 0:
		datatable.append(mask(data[pos:], key, (128 | type) & 240));
	return datatable;

def unmaskChunked(datatable):
	b = [];
	for x in range(len(datatable)):
		b.append(unmask(datatable[x]));
	return ''.join(b);

def pong(mask, masked):
	a = b'\x8a'; #Fin marker and pong op code
	if masked:
		a += b'\x80' + mask;
	else:
		a += b'\x00\x00\x00\x00\x00';
	return a;

def ping():
	a = '\x89'; #Fin marker and ping op code
	#TODO

def genSecWebsocketAccept(original):
	return base64.b64encode(hashlib.sha1(original + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest());

class per_message_inflator(object):
	def __init__(self, *args, **kwargs):
		object.__init__(self);
		self.__options = (args, kwargs);
		self.regenCompObj();

	def regenCompObj(self):
		try:
			del self.__zlib;
		except:
			pass;
		gc.collect();
		self.__zlib = zlib.decompressobj(*self.__options[0], **self.__options[1]);

	def inflate(self, data):
		try:
			a = self.__zlib.decompress(data + '\x00\x00\xff\xff');
			a += self.__zlib.flush();
			return a;
		except Exception as e:
			print(e);
			self.regenCompObj();
			a = self.__zlib.decompress(data + '\x00\x00\xff\xff');
			a += self.__zlib.flush();
			return a;

	decompress = inflate;
