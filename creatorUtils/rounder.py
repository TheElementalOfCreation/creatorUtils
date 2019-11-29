import math
from creatorUtils.compat.types import *

class Rounder(object):
	def __init__(self, threshold = 0.5, inclusive = True):
		object.__init__(self)
		if threshold >= 1.0 or threshold <= 0.0:
			raise ValueError('Threshold may not be less than or equal to zero and may not be greater than or equal to 1.')
		self.__threshold = threshold
		self.__inclusive = inclusive

	def roundFloat(self, inp):
		if isinstance(inp, intlong):
			return float(inp)
		if not isinstance(inp, float):
			inp = float(inp)
		sign = -1 if inp < 0 else 1
		inp = abs(inp)
		if (inp % 1 > self.__threshold) or ((inp % 1 == self.__threshold) and self.__inclusive):
			inp += 1
		inp = float(int(inp))
		inp *= sign
		return inp

	round = roundFloat

	def roundInt(self, inp):
		return int(self.round(inp))
