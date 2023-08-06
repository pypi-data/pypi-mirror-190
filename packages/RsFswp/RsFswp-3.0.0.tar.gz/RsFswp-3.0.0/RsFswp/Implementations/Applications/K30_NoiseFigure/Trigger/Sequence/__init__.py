from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SequenceCls:
	"""Sequence commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sequence", core, parent)

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def holdoff(self):
		"""holdoff commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_holdoff'):
			from .Holdoff import HoldoffCls
			self._holdoff = HoldoffCls(self._core, self._cmd_group)
		return self._holdoff

	@property
	def dtime(self):
		"""dtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dtime'):
			from .Dtime import DtimeCls
			self._dtime = DtimeCls(self._core, self._cmd_group)
		return self._dtime

	@property
	def slope(self):
		"""slope commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slope'):
			from .Slope import SlopeCls
			self._slope = SlopeCls(self._core, self._cmd_group)
		return self._slope

	def clone(self) -> 'SequenceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SequenceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
