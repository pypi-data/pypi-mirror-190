

import typing

import jk_typing

from .TextSpanInfo import TextSpanInfo





#
# This class represents space/non-space information about a sequence of characters boolean values.
#
class TextSpanInfoSequence(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			values:typing.Iterable[TextSpanInfo],
		):

		if isinstance(values, list):
			self.values = values
		else:
			self.values = list(values)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __iter__(self):
		yield from self.values
	#

	def __len__(self):
		return len(self.values)
	#

	def __str__(self) -> str:
		return "TextSpanInfoSequence<( {} )>".format(self.values)
	#

	def __repr__(self) -> str:
		return self.__str__()
	#

	def thinoutSpaceSegments(self, minLength:int):				# -> TextSpanInfoSequence
		ret = list(self.values)

		# set unwanted spaces to non-spaces

		for i in range(0, len(ret)):
			c = ret[i]
			if c.bIsSpace:
				if c.length < minLength:
					ret[i] = TextSpanInfo(False, c.pos, c.length)

		# now aggregate

		i = 0
		while i < len(ret) - 1:
			cur = ret[i]
			next = ret[i+1]
			if cur.bIsNonSpace and next.bIsNonSpace:
				# merge
				cur = TextSpanInfo(False, cur.pos, cur.length + next.length)
				ret[i] = cur
				del ret[i+1]
			else:
				i += 1

		return TextSpanInfoSequence(ret)
	#

	def extractOnlyNonSpaceSegments(self):				# -> TextSpanInfoSequence
		ret = []

		for c in self.values:
			if not c.bIsSpace:
				ret.append(c)

		return TextSpanInfoSequence(ret)
	#

#







