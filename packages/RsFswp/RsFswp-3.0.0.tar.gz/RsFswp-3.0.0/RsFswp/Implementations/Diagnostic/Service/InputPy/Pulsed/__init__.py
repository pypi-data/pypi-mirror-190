from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PulsedCls:
	"""Pulsed commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pulsed", core, parent)

	@property
	def cfrequency(self):
		"""cfrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfrequency'):
			from .Cfrequency import CfrequencyCls
			self._cfrequency = CfrequencyCls(self._core, self._cmd_group)
		return self._cfrequency

	@property
	def mcFrequency(self):
		"""mcFrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcFrequency'):
			from .McFrequency import McFrequencyCls
			self._mcFrequency = McFrequencyCls(self._core, self._cmd_group)
		return self._mcFrequency

	@property
	def wbFrequency(self):
		"""wbFrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wbFrequency'):
			from .WbFrequency import WbFrequencyCls
			self._wbFrequency = WbFrequencyCls(self._core, self._cmd_group)
		return self._wbFrequency

	def clone(self) -> 'PulsedCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PulsedCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
