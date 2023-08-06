from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaccuracyCls:
	"""Maccuracy commands group definition. 110 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maccuracy", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def default(self):
		"""default commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_default'):
			from .Default import DefaultCls
			self._default = DefaultCls(self._core, self._cmd_group)
		return self._default

	@property
	def cfError(self):
		"""cfError commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfError'):
			from .CfError import CfErrorCls
			self._cfError = CfErrorCls(self._core, self._cmd_group)
		return self._cfError

	@property
	def evm(self):
		"""evm commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_evm'):
			from .Evm import EvmCls
			self._evm = EvmCls(self._core, self._cmd_group)
		return self._evm

	@property
	def fdError(self):
		"""fdError commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdError'):
			from .FdError import FdErrorCls
			self._fdError = FdErrorCls(self._core, self._cmd_group)
		return self._fdError

	@property
	def freqError(self):
		"""freqError commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqError'):
			from .FreqError import FreqErrorCls
			self._freqError = FreqErrorCls(self._core, self._cmd_group)
		return self._freqError

	@property
	def merror(self):
		"""merror commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_merror'):
			from .Merror import MerrorCls
			self._merror = MerrorCls(self._core, self._cmd_group)
		return self._merror

	@property
	def ooffset(self):
		"""ooffset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ooffset'):
			from .Ooffset import OoffsetCls
			self._ooffset = OoffsetCls(self._core, self._cmd_group)
		return self._ooffset

	@property
	def perror(self):
		"""perror commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_perror'):
			from .Perror import PerrorCls
			self._perror = PerrorCls(self._core, self._cmd_group)
		return self._perror

	@property
	def rho(self):
		"""rho commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rho'):
			from .Rho import RhoCls
			self._rho = RhoCls(self._core, self._cmd_group)
		return self._rho

	def clone(self) -> 'MaccuracyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MaccuracyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
