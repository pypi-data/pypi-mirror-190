from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnrCls:
	"""Enr commands group definition. 23 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enr", core, parent)

	@property
	def calibration(self):
		"""calibration commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def measurement(self):
		"""measurement commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_measurement'):
			from .Measurement import MeasurementCls
			self._measurement = MeasurementCls(self._core, self._cmd_group)
		return self._measurement

	@property
	def common(self):
		"""common commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_common'):
			from .Common import CommonCls
			self._common = CommonCls(self._core, self._cmd_group)
		return self._common

	@property
	def sns(self):
		"""sns commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sns'):
			from .Sns import SnsCls
			self._sns = SnsCls(self._core, self._cmd_group)
		return self._sns

	def clone(self) -> 'EnrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EnrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
