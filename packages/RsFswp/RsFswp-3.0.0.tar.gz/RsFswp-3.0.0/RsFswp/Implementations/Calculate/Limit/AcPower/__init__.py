from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AcPowerCls:
	"""AcPower commands group definition. 37 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acPower", core, parent)

	@property
	def gap(self):
		"""gap commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_gap'):
			from .Gap import GapCls
			self._gap = GapCls(self._core, self._cmd_group)
		return self._gap

	@property
	def achannel(self):
		"""achannel commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_achannel'):
			from .Achannel import AchannelCls
			self._achannel = AchannelCls(self._core, self._cmd_group)
		return self._achannel

	@property
	def alternate(self):
		"""alternate commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_alternate'):
			from .Alternate import AlternateCls
			self._alternate = AlternateCls(self._core, self._cmd_group)
		return self._alternate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'AcPowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AcPowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
