from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def achannel(self):
		"""achannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_achannel'):
			from .Achannel import AchannelCls
			self._achannel = AchannelCls(self._core, self._cmd_group)
		return self._achannel

	@property
	def uaChannel(self):
		"""uaChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uaChannel'):
			from .UaChannel import UaChannelCls
			self._uaChannel = UaChannelCls(self._core, self._cmd_group)
		return self._uaChannel

	@property
	def alternate(self):
		"""alternate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alternate'):
			from .Alternate import AlternateCls
			self._alternate = AlternateCls(self._core, self._cmd_group)
		return self._alternate

	@property
	def ualternate(self):
		"""ualternate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ualternate'):
			from .Ualternate import UalternateCls
			self._ualternate = UalternateCls(self._core, self._cmd_group)
		return self._ualternate

	@property
	def gap(self):
		"""gap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gap'):
			from .Gap import GapCls
			self._gap = GapCls(self._core, self._cmd_group)
		return self._gap

	def clone(self) -> 'NameCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NameCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
