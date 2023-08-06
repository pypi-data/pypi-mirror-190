from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DexportCls:
	"""Dexport commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dexport", core, parent)

	@property
	def cseparator(self):
		"""cseparator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cseparator'):
			from .Cseparator import CseparatorCls
			self._cseparator = CseparatorCls(self._core, self._cmd_group)
		return self._cseparator

	@property
	def dseparator(self):
		"""dseparator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dseparator'):
			from .Dseparator import DseparatorCls
			self._dseparator = DseparatorCls(self._core, self._cmd_group)
		return self._dseparator

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def header(self):
		"""header commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_header'):
			from .Header import HeaderCls
			self._header = HeaderCls(self._core, self._cmd_group)
		return self._header

	@property
	def traces(self):
		"""traces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_traces'):
			from .Traces import TracesCls
			self._traces = TracesCls(self._core, self._cmd_group)
		return self._traces

	def clone(self) -> 'DexportCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DexportCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
