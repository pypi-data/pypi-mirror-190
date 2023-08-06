from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcalibrationCls:
	"""Pcalibration commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcalibration", core, parent)

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Condition import ConditionCls
			self._condition = ConditionCls(self._core, self._cmd_group)
		return self._condition

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Event import EventCls
			self._event = EventCls(self._core, self._cmd_group)
		return self._event

	@property
	def ptransistion(self):
		"""ptransistion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransistion'):
			from .Ptransistion import PtransistionCls
			self._ptransistion = PtransistionCls(self._core, self._cmd_group)
		return self._ptransistion

	@property
	def ntransistion(self):
		"""ntransistion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransistion'):
			from .Ntransistion import NtransistionCls
			self._ntransistion = NtransistionCls(self._core, self._cmd_group)
		return self._ntransistion

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import EnableCls
			self._enable = EnableCls(self._core, self._cmd_group)
		return self._enable

	def clone(self) -> 'PcalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PcalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
