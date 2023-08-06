from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def due(self):
		"""due commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_due'):
			from .Due import DueCls
			self._due = DueCls(self._core, self._cmd_group)
		return self._due

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Interval import IntervalCls
			self._interval = IntervalCls(self._core, self._cmd_group)
		return self._interval

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
