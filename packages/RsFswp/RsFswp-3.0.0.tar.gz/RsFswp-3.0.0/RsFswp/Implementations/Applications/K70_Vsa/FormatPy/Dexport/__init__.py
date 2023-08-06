from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DexportCls:
	"""Dexport commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dexport", core, parent)

	@property
	def dseparator(self):
		"""dseparator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dseparator'):
			from .Dseparator import DseparatorCls
			self._dseparator = DseparatorCls(self._core, self._cmd_group)
		return self._dseparator

	@property
	def header(self):
		"""header commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_header'):
			from .Header import HeaderCls
			self._header = HeaderCls(self._core, self._cmd_group)
		return self._header

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	def clone(self) -> 'DexportCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DexportCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
