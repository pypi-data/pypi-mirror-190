from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DisplayCls:
	"""Display commands group definition. 5 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	@property
	def fpanel(self):
		"""fpanel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fpanel'):
			from .Fpanel import FpanelCls
			self._fpanel = FpanelCls(self._core, self._cmd_group)
		return self._fpanel

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Update import UpdateCls
			self._update = UpdateCls(self._core, self._cmd_group)
		return self._update

	@property
	def lock(self):
		"""lock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lock'):
			from .Lock import LockCls
			self._lock = LockCls(self._core, self._cmd_group)
		return self._lock

	@property
	def message(self):
		"""message commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_message'):
			from .Message import MessageCls
			self._message = MessageCls(self._core, self._cmd_group)
		return self._message

	def clone(self) -> 'DisplayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DisplayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
