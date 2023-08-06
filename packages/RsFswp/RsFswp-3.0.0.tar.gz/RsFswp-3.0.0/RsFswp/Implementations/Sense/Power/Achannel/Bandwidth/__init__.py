from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BandwidthCls:
	"""Bandwidth commands group definition. 5 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	@property
	def uaChannel(self):
		"""uaChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uaChannel'):
			from .UaChannel import UaChannelCls
			self._uaChannel = UaChannelCls(self._core, self._cmd_group)
		return self._uaChannel

	@property
	def ualternate(self):
		"""ualternate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ualternate'):
			from .Ualternate import UalternateCls
			self._ualternate = UalternateCls(self._core, self._cmd_group)
		return self._ualternate

	@property
	def gap(self):
		"""gap commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gap'):
			from .Gap import GapCls
			self._gap = GapCls(self._core, self._cmd_group)
		return self._gap

	def clone(self) -> 'BandwidthCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BandwidthCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
