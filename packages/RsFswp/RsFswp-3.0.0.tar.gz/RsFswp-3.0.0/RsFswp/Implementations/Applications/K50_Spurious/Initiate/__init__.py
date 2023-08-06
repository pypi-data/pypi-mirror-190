from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitiateCls:
	"""Initiate commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initiate", core, parent)

	@property
	def continuous(self):
		"""continuous commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_continuous'):
			from .Continuous import ContinuousCls
			self._continuous = ContinuousCls(self._core, self._cmd_group)
		return self._continuous

	@property
	def conMeas(self):
		"""conMeas commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conMeas'):
			from .ConMeas import ConMeasCls
			self._conMeas = ConMeasCls(self._core, self._cmd_group)
		return self._conMeas

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Immediate import ImmediateCls
			self._immediate = ImmediateCls(self._core, self._cmd_group)
		return self._immediate

	@property
	def spurious(self):
		"""spurious commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spurious'):
			from .Spurious import SpuriousCls
			self._spurious = SpuriousCls(self._core, self._cmd_group)
		return self._spurious

	@property
	def sync(self):
		"""sync commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import SyncCls
			self._sync = SyncCls(self._core, self._cmd_group)
		return self._sync

	def clone(self) -> 'InitiateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InitiateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
