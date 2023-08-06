from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CreateCls:
	"""Create commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("create", core, parent)

	@property
	def new(self):
		"""new commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_new'):
			from .New import NewCls
			self._new = NewCls(self._core, self._cmd_group)
		return self._new

	@property
	def replace(self):
		"""replace commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_replace'):
			from .Replace import ReplaceCls
			self._replace = ReplaceCls(self._core, self._cmd_group)
		return self._replace

	@property
	def duplicate(self):
		"""duplicate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duplicate'):
			from .Duplicate import DuplicateCls
			self._duplicate = DuplicateCls(self._core, self._cmd_group)
		return self._duplicate

	def clone(self) -> 'CreateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CreateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
