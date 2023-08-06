from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqAnalyzerCls:
	"""IqAnalyzer commands group definition. 4 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqAnalyzer", core, parent)

	@property
	def layout(self):
		"""layout commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_layout'):
			from .Layout import LayoutCls
			self._layout = LayoutCls(self._core, self._cmd_group)
		return self._layout

	def clone(self) -> 'IqAnalyzerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqAnalyzerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
