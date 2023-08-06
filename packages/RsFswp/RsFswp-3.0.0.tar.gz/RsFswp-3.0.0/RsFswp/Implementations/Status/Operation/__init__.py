from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OperationCls:
	"""Operation commands group definition. 10 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("operation", core, parent)

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Event import EventCls
			self._event = EventCls(self._core, self._cmd_group)
		return self._event

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Condition import ConditionCls
			self._condition = ConditionCls(self._core, self._cmd_group)
		return self._condition

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import EnableCls
			self._enable = EnableCls(self._core, self._cmd_group)
		return self._enable

	@property
	def ptransition(self):
		"""ptransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransition'):
			from .Ptransition import PtransitionCls
			self._ptransition = PtransitionCls(self._core, self._cmd_group)
		return self._ptransition

	@property
	def ntransition(self):
		"""ntransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransition'):
			from .Ntransition import NtransitionCls
			self._ntransition = NtransitionCls(self._core, self._cmd_group)
		return self._ntransition

	@property
	def pcalibration(self):
		"""pcalibration commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcalibration'):
			from .Pcalibration import PcalibrationCls
			self._pcalibration = PcalibrationCls(self._core, self._cmd_group)
		return self._pcalibration

	def clone(self) -> 'OperationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OperationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
