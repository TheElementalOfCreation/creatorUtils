import copy

from creatorUtils.compat.types import *

class RepeatingGenerator(object):
    """
    Returns an entry in the list, starting from the first, and looping to the beginning when the end is reached
    """
    def __init__(self, data_list):
        print('WARNING: You probably want to use itertools.cycle instead of this class.')
        object.__init__(self)
        if not isinstance(data_list, list_types):
            raise TypeError('`data_list` must either be a list or tuple.')
        self.__position = 0
        self.__data = data_list if isinstance(data_list, tuple) else copy.deepcopy(data_list)
        self.__datalen = len(self.__data)

    def next(self):
        r = self.__data[self.__position]
        self.__position = (self.__position + 1) % self.__datalen
        return r

    __call__ = next

    def reset(self):
        self.__position = -1

    @property
    def length(self):
        return self.__datalen

    @property
    def position(self):
        return self.__position



try:
    import itertools
    repeater = itertools.cycle
except ModuleNotFoundError:
    repeater = RepeatingGenerator



# class Byte(tuple):
#     def __new__(tupletype, integer):
#         return tuple.__new__(tupletype, [int(x) for x in bin(integer)[2:].rjust(8, '0')])
#
# BYTES = tuple([Byte(x) for x in range(256)])
#
# if version_info[0] < 3:
#     def toArrayOfBytes(inp):
#         if isinstance(inp, bytearray):
#             return [BYTES[x] for x in inp]
#         elif isinstance(inp, str):
#             return [BYTES[ord(x)] for x in inp]
#         elif isinstance(inp, ImmutableBitArray):
#             return inp
#         else:
#             raise TypeError('Input must be either a bytearray or string.')
#
# else:
#     def toArrayOfBytes(inp):
#         if isinstance(inp, bytes):
#             return [BYTES[x] for x in inp]
#         else:
#             raise TypeError('Input must be either a bytearray or string.')
#
#
# class BitArray(object):
#     def __init__(self, inp):
#         object.__init__(self):
#
#     def __add__(self, inp):
#
#
#
#
# class ImmutableBitArray(tuple):
#     def __new__(tupletype, inp):
#         return tuple.__new__(tupletype, toArrayOfBytes(inp))
