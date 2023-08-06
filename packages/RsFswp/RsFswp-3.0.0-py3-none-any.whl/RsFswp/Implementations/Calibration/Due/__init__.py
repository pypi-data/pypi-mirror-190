from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DueCls:
	"""Due commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("due", core, parent)

	@property
	def schedule(self):
		"""schedule commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schedule'):
			from .Schedule import ScheduleCls
			self._schedule = ScheduleCls(self._core, self._cmd_group)
		return self._schedule

	@property
	def shutdown(self):
		"""shutdown commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shutdown'):
			from .Shutdown import ShutdownCls
			self._shutdown = ShutdownCls(self._core, self._cmd_group)
		return self._shutdown

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def days(self):
		"""days commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_days'):
			from .Days import DaysCls
			self._days = DaysCls(self._core, self._cmd_group)
		return self._days

	@property
	def warmup(self):
		"""warmup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_warmup'):
			from .Warmup import WarmupCls
			self._warmup = WarmupCls(self._core, self._cmd_group)
		return self._warmup

	def clone(self) -> 'DueCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DueCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
