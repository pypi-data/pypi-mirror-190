from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PeakSearchCls:
	"""PeakSearch commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("peakSearch", core, parent)

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import AutoCls
			self._auto = AutoCls(self._core, self._cmd_group)
		return self._auto

	@property
	def subranges(self):
		"""subranges commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subranges'):
			from .Subranges import SubrangesCls
			self._subranges = SubrangesCls(self._core, self._cmd_group)
		return self._subranges

	@property
	def margin(self):
		"""margin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_margin'):
			from .Margin import MarginCls
			self._margin = MarginCls(self._core, self._cmd_group)
		return self._margin

	@property
	def pshow(self):
		"""pshow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pshow'):
			from .Pshow import PshowCls
			self._pshow = PshowCls(self._core, self._cmd_group)
		return self._pshow

	def clone(self) -> 'PeakSearchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PeakSearchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
