from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LossCls:
	"""Loss commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("loss", core, parent)

	@property
	def high(self):
		"""high commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_high'):
			from .High import HighCls
			self._high = HighCls(self._core, self._cmd_group)
		return self._high

	@property
	def low(self):
		"""low commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_low'):
			from .Low import LowCls
			self._low = LowCls(self._core, self._cmd_group)
		return self._low

	@property
	def table(self):
		"""table commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_table'):
			from .Table import TableCls
			self._table = TableCls(self._core, self._cmd_group)
		return self._table

	def clone(self) -> 'LossCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LossCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
