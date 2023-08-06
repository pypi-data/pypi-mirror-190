from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def vswr(self):
		"""vswr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vswr'):
			from .Vswr import VswrCls
			self._vswr = VswrCls(self._core, self._cmd_group)
		return self._vswr

	@property
	def rl(self):
		"""rl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rl'):
			from .Rl import RlCls
			self._rl = RlCls(self._core, self._cmd_group)
		return self._rl

	@property
	def sns(self):
		"""sns commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sns'):
			from .Sns import SnsCls
			self._sns = SnsCls(self._core, self._cmd_group)
		return self._sns

	@property
	def calibration(self):
		"""calibration commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
