from creatorUtils.compat.types import *;
import copy;

class RepeatingGenerator(object):
	"""
	Returns an entry in the list, starting from the first, and looping to the beginning when the end is reached
	"""
	def __init__(self, data_list):
		object.__init__(self);
		if not isinstance(data_list, list_types):
			raise TypeError('`data_list` must either be a list or tuple.');
		self.__position = 0;
		self.__data = data_list if isinstance(data_list, tuple) else copy.deepcopy(data_list);
		self.__datalen = len(self.__data);

	def next(self):
		r = self.__data[self.__position];
		self.__position = (self.__position + 1) % self.__datalen;
		return r;

	__call__ = next;

	def reset(self):
		self.__position = -1;

	@property
	def length(self):
		return self.__datalen;

	@property
	def position(self):
		return self.__position;
