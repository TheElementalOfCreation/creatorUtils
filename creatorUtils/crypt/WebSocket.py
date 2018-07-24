import zlib;
from creatorUtils import forma;

def unmask(data, masked = None):
	data = bytearray(data);
	if masked == None:
		masked = 128 == (data[1] & 128);
	datalen = (0x7F & data[1]);
	if datalen == 126:
		x = 4;
	elif datalen == 127:
		x = 10;
	else:
		x = 2;
	if masked:
		str_data = '';
		if datalen > 0:
			mask_key = data[x:x+4];
			masked_data = data[x+4:];
			unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))];
			str_data = str(bytearray(unmasked_data));
	else:
		str_data = str(data)[x:];
	return str_data;


def mask(data, key = '', byte = 0b10000010):
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
	are reserved, and `efgh` signifies the data type.

	The following is a list of possible datatypes:
	 + 0b0000 = Continuation
	 + 0b0001 = Text
	 + 0b0010 = Binary
	 + 0b0011 = Unknown
	 + 0b0100 = Unknown
	 + 0b0101 = Unknown
	 + 0b0110 = Unknown
	 + 0b0111 = Unknown
	 + 0b1000 = Connection Close
	 + 0b1001 = Ping
	 + 0b1010 = Pong
	 + 0b1011 = Unknown
	 + 0b1100 = Unknown
	 + 0b1101 = Unknown
	 + 0b1110 = Unknown
	 + 0b1111 = Unknown
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
		str_data = chr(byte) + chr(128 + datalen) + ad + str(key);
	else:
		str_data = chr(byte) + chr(datalen) + ad + str(key);
	if datalen > 0:
		if len(key) > 0:
			mask_key = bytearray(key);
			unmasked_data = bytearray(data);
			masked_data = [unmasked_data[i] ^ mask_key[i%4] for i in range(len(unmasked_data))];
			str_data += str(bytearray(masked_data));
		else:
			str_data += str(bytearray(data));
	return str_data;

def limitedMask(data, key = '1y6S', max = 1000, type = 2):
	type = type & 15;
	if max % 4 != 0:
		raise Exception('`max` must be a multiple of 4');
	datatable = [];
	pos = 0;
	if len(data) - pos > max:
		datatable.append(mask(data[pos:pos + max], key, type));
		pos += max;
	else:
		datatable.append(mask(data[pos:pos + max], key, 128 | type));
	while len(data) - pos > max:
		datatable.append(mask(data[pos:pos + max], key, type & 11110000));
		pos += max;
	if pos != 0:
		datatable.append(mask(data[pos:], key, (128 | type) & 11110000));
	return datatable;

def unmaskChunked(datatable):
	b = [];
	for x in range(len(datatable)):
		b.append(unmask(datatable[x]));
	return ''.join(b);

def pong(mask, masked):
	a = '\x8a'; #Fin marker and pong op code
	if masked:
		a += '\x80' + mask;
	else:
		a += '\x00\x00\x00\x00\x00'
	return a;

def ping():
	a = '\x89' #Fin marker and ping op code
	#TODO
