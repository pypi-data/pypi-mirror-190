from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SweepCls:
	"""Sweep commands group definition. 7 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sweep", core, parent)

	@property
	def stop(self):
		"""stop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stop'):
			from .Stop import StopCls
			self._stop = StopCls(self._core, self._cmd_group)
		return self._stop

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def avg(self):
		"""avg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_avg'):
			from .Avg import AvgCls
			self._avg = AvgCls(self._core, self._cmd_group)
		return self._avg

	@property
	def fdrift(self):
		"""fdrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdrift'):
			from .Fdrift import FdriftCls
			self._fdrift = FdriftCls(self._core, self._cmd_group)
		return self._fdrift

	@property
	def mdrift(self):
		"""mdrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mdrift'):
			from .Mdrift import MdriftCls
			self._mdrift = MdriftCls(self._core, self._cmd_group)
		return self._mdrift

	@property
	def ldrift(self):
		"""ldrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldrift'):
			from .Ldrift import LdriftCls
			self._ldrift = LdriftCls(self._core, self._cmd_group)
		return self._ldrift

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Start import StartCls
			self._start = StartCls(self._core, self._cmd_group)
		return self._start

	def clone(self) -> 'SweepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SweepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
