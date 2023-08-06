from .__ import *


class Stamp(list[int, int]):

	def __init__(self, t0, t1, unit: Union[str, int] = 'ms'):
		___ = [t0, t1]
		if isinstance(unit, str):
			unit = unit.lower()
			assert unit in {'ms', 's'}
			if unit == 's':
				___ = [_ * 1000 for _ in ___]
				pass
			pass
		else:
			___ = [_ * 1000 / unit for _ in ___]
			pass
		___ = [round(_) for _ in ___]
		super().__init__(___)
		pass

	def shift(self, ms):
		return [_ + ms for _ in self]

	pass
