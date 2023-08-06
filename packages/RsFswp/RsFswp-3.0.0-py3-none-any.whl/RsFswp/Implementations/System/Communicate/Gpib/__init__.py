from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GpibCls:
	"""Gpib commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gpib", core, parent)

	@property
	def rdevice(self):
		"""rdevice commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rdevice'):
			from .Rdevice import RdeviceCls
			self._rdevice = RdeviceCls(self._core, self._cmd_group)
		return self._rdevice

	@property
	def self(self):
		"""self commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_self'):
			from .Self import SelfCls
			self._self = SelfCls(self._core, self._cmd_group)
		return self._self

	def clone(self) -> 'GpibCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GpibCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
