from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EvmCls:
	"""Evm commands group definition. 18 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("evm", core, parent)

	@property
	def rcurrent(self):
		"""rcurrent commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rcurrent'):
			from .Rcurrent import RcurrentCls
			self._rcurrent = RcurrentCls(self._core, self._cmd_group)
		return self._rcurrent

	@property
	def rmean(self):
		"""rmean commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rmean'):
			from .Rmean import RmeanCls
			self._rmean = RmeanCls(self._core, self._cmd_group)
		return self._rmean

	@property
	def rpeak(self):
		"""rpeak commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rpeak'):
			from .Rpeak import RpeakCls
			self._rpeak = RpeakCls(self._core, self._cmd_group)
		return self._rpeak

	@property
	def pcurrent(self):
		"""pcurrent commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcurrent'):
			from .Pcurrent import PcurrentCls
			self._pcurrent = PcurrentCls(self._core, self._cmd_group)
		return self._pcurrent

	@property
	def pmean(self):
		"""pmean commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pmean'):
			from .Pmean import PmeanCls
			self._pmean = PmeanCls(self._core, self._cmd_group)
		return self._pmean

	@property
	def ppeak(self):
		"""ppeak commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ppeak'):
			from .Ppeak import PpeakCls
			self._ppeak = PpeakCls(self._core, self._cmd_group)
		return self._ppeak

	def clone(self) -> 'EvmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EvmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
