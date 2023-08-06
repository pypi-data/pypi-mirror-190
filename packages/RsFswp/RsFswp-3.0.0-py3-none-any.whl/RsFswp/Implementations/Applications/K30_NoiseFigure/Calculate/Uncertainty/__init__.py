from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UncertaintyCls:
	"""Uncertainty commands group definition. 29 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uncertainty", core, parent)

	@property
	def sanalyzer(self):
		"""sanalyzer commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sanalyzer'):
			from .Sanalyzer import SanalyzerCls
			self._sanalyzer = SanalyzerCls(self._core, self._cmd_group)
		return self._sanalyzer

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	@property
	def common(self):
		"""common commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_common'):
			from .Common import CommonCls
			self._common = CommonCls(self._core, self._cmd_group)
		return self._common

	@property
	def preamp(self):
		"""preamp commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_preamp'):
			from .Preamp import PreampCls
			self._preamp = PreampCls(self._core, self._cmd_group)
		return self._preamp

	@property
	def enr(self):
		"""enr commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_enr'):
			from .Enr import EnrCls
			self._enr = EnrCls(self._core, self._cmd_group)
		return self._enr

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def match(self):
		"""match commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_match'):
			from .Match import MatchCls
			self._match = MatchCls(self._core, self._cmd_group)
		return self._match

	def clone(self) -> 'UncertaintyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UncertaintyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
