from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalibrationCls:
	"""Calibration commands group definition. 9 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def aiq(self):
		"""aiq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aiq'):
			from .Aiq import AiqCls
			self._aiq = AiqCls(self._core, self._cmd_group)
		return self._aiq

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def due(self):
		"""due commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_due'):
			from .Due import DueCls
			self._due = DueCls(self._core, self._cmd_group)
		return self._due

	@property
	def preSelection(self):
		"""preSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preSelection'):
			from .PreSelection import PreSelectionCls
			self._preSelection = PreSelectionCls(self._core, self._cmd_group)
		return self._preSelection

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	def clone(self) -> 'CalibrationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalibrationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
