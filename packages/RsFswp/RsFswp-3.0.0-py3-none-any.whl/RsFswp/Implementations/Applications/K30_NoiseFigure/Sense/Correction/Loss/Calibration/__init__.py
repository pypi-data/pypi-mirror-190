from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 7 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def spot(self):
		"""spot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spot'):
			from .Spot import SpotCls
			self._spot = SpotCls(self._core, self._cmd_group)
		return self._spot

	@property
	def table(self):
		"""table commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_table'):
			from .Table import TableCls
			self._table = TableCls(self._core, self._cmd_group)
		return self._table

	@property
	def temperature(self):
		"""temperature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_temperature'):
			from .Temperature import TemperatureCls
			self._temperature = TemperatureCls(self._core, self._cmd_group)
		return self._temperature

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
