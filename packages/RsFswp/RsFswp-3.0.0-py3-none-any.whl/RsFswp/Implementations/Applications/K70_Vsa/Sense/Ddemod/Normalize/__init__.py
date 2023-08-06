from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NormalizeCls:
	"""Normalize commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("normalize", core, parent)

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .Value import ValueCls
			self._value = ValueCls(self._core, self._cmd_group)
		return self._value

	@property
	def cfdrift(self):
		"""cfdrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfdrift'):
			from .Cfdrift import CfdriftCls
			self._cfdrift = CfdriftCls(self._core, self._cmd_group)
		return self._cfdrift

	@property
	def fdError(self):
		"""fdError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdError'):
			from .FdError import FdErrorCls
			self._fdError = FdErrorCls(self._core, self._cmd_group)
		return self._fdError

	@property
	def iqOffset(self):
		"""iqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqOffset'):
			from .IqOffset import IqOffsetCls
			self._iqOffset = IqOffsetCls(self._core, self._cmd_group)
		return self._iqOffset

	@property
	def iqImbalance(self):
		"""iqImbalance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqImbalance'):
			from .IqImbalance import IqImbalanceCls
			self._iqImbalance = IqImbalanceCls(self._core, self._cmd_group)
		return self._iqImbalance

	@property
	def adroop(self):
		"""adroop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adroop'):
			from .Adroop import AdroopCls
			self._adroop = AdroopCls(self._core, self._cmd_group)
		return self._adroop

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def srError(self):
		"""srError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srError'):
			from .SrError import SrErrorCls
			self._srError = SrErrorCls(self._core, self._cmd_group)
		return self._srError

	def clone(self) -> 'NormalizeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NormalizeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
