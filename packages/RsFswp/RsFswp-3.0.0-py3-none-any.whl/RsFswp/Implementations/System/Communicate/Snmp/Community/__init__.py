from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CommunityCls:
	"""Community commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("community", core, parent)

	@property
	def ro(self):
		"""ro commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ro'):
			from .Ro import RoCls
			self._ro = RoCls(self._core, self._cmd_group)
		return self._ro

	@property
	def rw(self):
		"""rw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rw'):
			from .Rw import RwCls
			self._rw = RwCls(self._core, self._cmd_group)
		return self._rw

	def clone(self) -> 'CommunityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CommunityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
