from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PluginCls:
	"""Plugin commands group definition. 7 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plugin", core, parent)

	@property
	def appStarter(self):
		"""appStarter commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_appStarter'):
			from .AppStarter import AppStarterCls
			self._appStarter = AppStarterCls(self._core, self._cmd_group)
		return self._appStarter

	def clone(self) -> 'PluginCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PluginCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
