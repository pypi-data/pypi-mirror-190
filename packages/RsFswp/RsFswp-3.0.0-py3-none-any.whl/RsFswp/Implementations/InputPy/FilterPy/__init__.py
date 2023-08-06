from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def hpass(self):
		"""hpass commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hpass'):
			from .Hpass import HpassCls
			self._hpass = HpassCls(self._core, self._cmd_group)
		return self._hpass

	@property
	def yig(self):
		"""yig commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_yig'):
			from .Yig import YigCls
			self._yig = YigCls(self._core, self._cmd_group)
		return self._yig

	def clone(self) -> 'FilterPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
